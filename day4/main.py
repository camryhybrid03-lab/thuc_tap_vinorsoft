from fastapi import FastAPI, Path, Query, Header, Cookie, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI(title="Personal Blog API - Day 4")

# --- 1. PYDANTIC MODELS (Data Validation) ---
# Pydantic giúp kiểm soát dữ liệu đầu vào cực kỳ chặt chẽ
class BlogPost(BaseModel):
    id: int
    title: str = Field(..., min_length=5, max_length=100, example="Học FastAPI trong 1 ngày")
    content: str = Field(..., min_length=10)
    author: str
    tags: List[str] = []

class BlogPostCreate(BaseModel):
    title: str
    content: str
    author: str

# Giả lập cơ sở dữ liệu
db_blogs = [
    {"id": 1, "title": "Chào mừng đến với Blog", "content": "Đây là bài viết đầu tiên của tôi.", "author": "Hieu", "tags": ["hello", "first"]},
]

# --- 2. CRUD OPERATIONS ---

# Lấy danh sách blog (Sử dụng Query Params)
# Query Params: limit và search
@app.get("/blogs", tags=["Blogs"])
def get_blogs(
    limit: int = Query(10, gt=0, le=100), 
    search: Optional[str] = None
):
    results = db_blogs[:limit]
    if search:
        results = [b for b in results if search.lower() in b['title'].lower()]
    return {"data": results, "total": len(results)}

# Lấy chi tiết một bài viết (Sử dụng Path Params)
# Path Params: blog_id
@app.get("/blogs/{blog_id}", tags=["Blogs"])
def get_blog_detail(blog_id: int = Path(..., gt=0, description="ID của bài viết cần tìm")):
    blog = next((b for b in db_blogs if b['id'] == blog_id), None)
    if not blog:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết!")
    return blog

# Tạo bài viết mới (Data Validation với Pydantic)
@app.post("/blogs", status_code=221, tags=["Blogs"])
def create_blog(blog_data: BlogPostCreate):
    new_id = len(db_blogs) + 1
    new_blog = {"id": new_id, **blog_data.dict(), "tags": []}
    db_blogs.append(new_blog)
    return {"message": "Tạo bài viết thành công!", "blog": new_blog}

# --- 3. ADVANCED: HEADER & COOKIE ---
# Minh họa cách đọc Header và Cookie
@app.get("/system/info")
def get_system_info(
    user_agent: Optional[str] = Header(None),
    session_id: Optional[str] = Cookie(None)
):
    return {
        "User-Agent": user_agent,
        "Session-ID": session_id,
        "Message": "Thông tin hệ thống được lấy từ Header và Cookie"
    }