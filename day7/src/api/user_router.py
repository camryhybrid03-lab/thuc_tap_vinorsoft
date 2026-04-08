import logging
import httpx  # Thư viện dùng để gọi API thật (Telegram, Mail Service)
import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserOut
from src.schemas.token import Token
from src.auth.utils import create_access_token, verify_password, pwd_context 

router = APIRouter(prefix="/users", tags=["Users"])

# ==========================================
# 🛡️ CẤU HÌNH LOGGING CHUYÊN NGHIỆP
# ==========================================
# Thay vì print, ta dùng logger để có thể lưu file và phân loại lỗi
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("system_audit.log"), # Lưu vào file vĩnh viễn
        logging.StreamHandler() # Hiển thị ra terminal để mình theo dõi
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# 🚀 HỆ THỐNG XỬ LÝ NGẦM THỰC CHIẾN
# ==========================================

async def professional_onboarding(email: str, username: str):
    """Quy trình Onboarding thật sự chạy ngầm"""
    logger.info(f"Bắt đầu xử lý cho User mới: {username}")
    
    # 1. GHI NHẬT KÝ (LOGGING)
    # Trong thực tế, log giúp 'tra án' khi hệ thống gặp lỗi
    logger.info(f"AUDIT_LOG | Action: REGISTER | User: {username} | Email: {email}")

    # 2. GỬI THÔNG BÁO WEBHOOK (TELEGRAM/SLACK)
    # Thay vì print, ta dùng httpx để gửi một tin nhắn thật
    async with httpx.AsyncClient() as client:
        try:
            # Ví dụ: Gửi thông báo đến một Webhook URL (giả định)
            # URL này thường dẫn tới bot Telegram của công ty
            webhook_url = "https://httpbin.org/post" # Link test, thay bằng link thật sau
            payload = {"text": f"🚀 Có thành viên mới: {username} ({email})"}
            await client.post(webhook_url, json=payload, timeout=5.0)
            logger.info("Đã gửi thông báo Webhook tới Admin thành công.")
        except Exception as e:
            logger.error(f"Lỗi khi gửi Webhook thông báo: {e}")

    # 3. CHUẨN BỊ MÃ XÁC THỰC (OTP)
    otp_code = str(uuid.uuid4())[:6].upper()
    logger.info(f"Mã OTP [{otp_code}] đã sẵn sàng để gửi tới dịch vụ Email (SendGrid/AWS SES).")

# ==========================================
# 🛠 API ENDPOINTS
# ==========================================

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, 
    bg: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(User).where(User.email == user.email))
    if res.scalars().first(): 
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email đã tồn tại!"
        )

    new_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=pwd_context.hash(user.password)
    )
    
    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        # Kích hoạt quy trình ngầm
        bg.add_task(professional_onboarding, new_user.email, new_user.username)

        return new_user
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Lỗi hệ thống"
        )

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    res = await db.execute(select(User).where(User.username == form_data.username))
    user = res.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Sai thông tin đăng nhập"
        )

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}