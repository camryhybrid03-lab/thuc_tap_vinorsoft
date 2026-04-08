from pydantic import BaseModel

# Schema dùng để nhận dữ liệu khi tạo bài Blog
class BlogCreate(BaseModel):
    title: str
    content: str
    author: str

# Schema dùng để trả dữ liệu về cho người dùng (có thêm ID)
class BlogResponse(BlogCreate):
    id: int

    class Config:
        from_attributes = True