from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.blog import BlogDB
from src.schemas.blog import BlogCreate
from typing import Optional

class BlogService:
    @staticmethod
    async def create(db: AsyncSession, blog_data: BlogCreate): # <--- Nhận object Schema
        # model_dump() sẽ biến dữ liệu từ Pydantic thành dictionary để SQL hiểu
        new_blog = BlogDB(**blog_data.model_dump()) 
        db.add(new_blog)
        await db.commit()
        await db.refresh(new_blog)
        return new_blog

    @staticmethod
    async def get_all(db: AsyncSession, limit: int = 10, search: Optional[str] = None):
        # Tạo câu lệnh query cơ bản
        query = select(BlogDB).limit(limit)
        
        # Nếu có từ khóa tìm kiếm thì lọc thêm
        if search:
            query = query.where(BlogDB.title.ilike(f"%{search}%"))
            
        result = await db.execute(query)
        return result.scalars().all()
    

    @staticmethod
    async def get_by_id(db: AsyncSession, blog_id: int):
        result = await db.execute(select(BlogDB).where(BlogDB.id == blog_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update(db: AsyncSession, blog_id: int, blog_data: BlogCreate): # <--- Tương tự cho update
        blog = await BlogService.get_by_id(db, blog_id)
        if blog:
            # Cập nhật nhanh bằng cách lặp qua các field
            for key, value in blog_data.model_dump().items():
                setattr(blog, key, value)
            await db.commit()
            await db.refresh(blog)
        return blog

    @staticmethod
    async def delete(db: AsyncSession, blog_id: int):
        blog = await BlogService.get_by_id(db, blog_id)
        if blog:
            await db.delete(blog)
            await db.commit()
            return True
        return False