from fastapi import FastAPI, Path, Query, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# --- CONFIGURATION ---
SECRET_KEY = "your-super-secret-key" # Trong thực tế hãy để vào file .env
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Kết nối SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- DATABASE MODELS ---
class BlogModel(Base):
    __tablename__ = "blogs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    content = Column(Text)
    author = Column(String(50))

# Tạo bảng
Base.metadata.create_all(bind=engine)

# --- SECURITY UTILS ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# --- SCHEMAS (Pydantic) ---
class BlogPost(BaseModel):
    title: str
    content: str
    author: str

    model_config = {"from_attributes": True} # Cách viết mới của Pydantic V2

# --- DEPENDENCY ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Pro Blog API")

# --- 1. AUTHENTICATION ENDPOINT ---
@app.post("/login", tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Giả lập check user (Thực tế nên có bảng Users)
    if form_data.username == "admin" and form_data.password == "123456":
        access_token = create_access_token(data={"sub": form_data.username})
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Sai tài khoản hoặc mật khẩu")

# --- 2. CRUD OPERATIONS ---

@app.get("/blogs", response_model=List[BlogPost], tags=["Blogs"])
def read_blogs(db: Session = Depends(get_db)):
    return db.query(BlogModel).all()

@app.post("/blogs", status_code=201, tags=["Blogs"])
def create_blog(blog: BlogPost, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Chỉ ai có Token mới vào được đây
    new_blog = BlogModel(**blog.dict())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# --- UPDATE (U) ---
@app.put("/blogs/{blog_id}", tags=["Blogs"])
def update_blog(blog_id: int, updated_data: BlogPost, db: Session = Depends(get_db)):
    db_query = db.query(BlogModel).filter(BlogModel.id == blog_id)
    if not db_query.first():
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    db_query.update(updated_data.dict(), synchronize_session=False)
    db.commit()
    return {"message": "Cập nhật thành công"}

# --- DELETE (D) ---
@app.delete("/blogs/{blog_id}", tags=["Blogs"])
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    db_query = db.query(BlogModel).filter(BlogModel.id == blog_id)
    if not db_query.first():
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết")
    db_query.delete(synchronize_session=False)
    db.commit()
    return {"message": "Đã xóa bài viết"}