from sqlalchemy import Column, Integer, String, Text
from src.models.base import Base

class BlogDB(Base):
    __tablename__ = "blogs" # Tên bảng trong database
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(50))
    # Sau này có thể thêm created_at, updated_at...