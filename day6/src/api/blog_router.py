from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from src.database import get_db
from src.services.blog_service import BlogService
# Import cả 2 schema: 1 để nhận dữ liệu, 1 để định dạng dữ liệu trả về
from src.schemas.blog import BlogCreate, BlogResponse 

router = APIRouter(prefix="/blogs", tags=["blogs"])

@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(blog_in: BlogCreate, db: AsyncSession = Depends(get_db)):
    # Truyền cả cục blog_in vào service
    return await BlogService.create(db, blog_in)

@router.get("/", response_model=List[BlogResponse])
async def get_all_blogs(
    limit: int = 10, 
    search: Optional[str] = None, 
    db: AsyncSession = Depends(get_db)
):
    return await BlogService.get_all(db, limit, search)

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    blog = await BlogService.get_by_id(db, blog_id)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int, 
    blog_in: BlogCreate, 
    db: AsyncSession = Depends(get_db)
):
    blog = await BlogService.update(db, blog_id, blog_in)
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id: int, db: AsyncSession = Depends(get_db)):
    success = await BlogService.delete(db, blog_id)
    if not success:
        raise HTTPException(status_code=404, detail="Blog not found")
    return None