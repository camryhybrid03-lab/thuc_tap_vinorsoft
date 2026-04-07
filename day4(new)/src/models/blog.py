from pydantic import BaseModel, Field
from typing import List

# Class gốc chứa các trường dùng chung
class BlogPostBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, example="Học FastAPI chuẩn Enterprise")
    content: str = Field(..., min_length=10, example="Nội dung bài viết chi tiết ở đây...")
    author: str = Field(..., example="Minh Hieu")
    tags: List[str] = []

# Class dùng khi người dùng gửi dữ liệu lên (không cần ID vì hệ thống tự tạo)
class BlogPostCreate(BlogPostBase):
    pass

# Class dùng khi trả dữ liệu về cho người dùng (phải có ID)
class BlogPost(BlogPostBase):
    id: int