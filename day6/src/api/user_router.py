from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm

from src.database import get_db
from src.models.user import User
from src.schemas.user import UserCreate, UserOut
from src.schemas.token import Token
from src.auth.utils import create_access_token, verify_password, pwd_context 

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut, status_code=201)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check trùng
    res = await db.execute(select(User).where(User.email == user.email))
    if res.scalars().first(): raise HTTPException(400, "Email đã tồn tại!")

    new_user = User(
        username=user.username, 
        email=user.email, 
        hashed_password=pwd_context.hash(user.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Tìm theo username
    res = await db.execute(select(User).where(User.username == form_data.username))
    user = res.scalars().first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Sai tài khoản hoặc mật khẩu")

    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}