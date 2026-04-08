from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# Khai báo thuật toán mã hóa bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Mã hóa mật khẩu"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Kiểm tra mật khẩu nhập vào có khớp với mã hóa trong DB không"""
    return pwd_context.verify(plain_password, hashed_password)

SECRET_KEY = "Hieu_Secret_Key_2026" # Chuỗi này để khóa mã, đặt gì cũng được
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 # Token có hiệu lực trong 60 phút

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
# --------------------