from fastapi import APIRouter, Path, Query, HTTPException, status
from typing import List, Optional

# Cấu trúc import của Python (đi từ thư mục src)
from src.models.blog import BlogPost, BlogPostCreate
from src.services.blog_service import BlogService

# Tạo router với tiền tố /blogs
router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.get("/", response_model=List[BlogPost])
def get_all_blogs(
    limit: int = Query(10, gt=0, description="Số lượng bài viết tối đa"), 
    search: Optional[str] = Query(None, description="Từ khóa tìm kiếm trong tiêu đề")
):
    return BlogService.get_all(limit, search)

@router.get("/{blog_id}", response_model=BlogPost)
def get_blog_detail(blog_id: int = Path(..., gt=0, description="ID bài viết")):
    blog = BlogService.get_by_id(blog_id)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bài viết")
    return blog

@router.post("/", response_model=BlogPost, status_code=status.HTTP_201_CREATED)
def create_new_blog(payload: BlogPostCreate):
    return BlogService.create(payload)

# Thêm chức năng Xóa bài viết
@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(blog_id: int = Path(..., gt=0)):
    success = BlogService.delete(blog_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy bài viết để xóa")
    
@router.put("/{blog_id}", response_model=BlogPost)
def update_blog(blog_id: int, payload: BlogPostCreate):
    updated_blog = BlogService.update(blog_id, payload)
    if not updated_blog:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài viết để sửa")
    return updated_blog