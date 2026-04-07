from typing import List, Optional
from src.models.blog import BlogPost, BlogPostCreate

# Giả lập Database lưu trong RAM
db_blogs: List[BlogPost] = []
id_counter = 1

class BlogService:
    @staticmethod
    def get_all(limit: int = 10, search: Optional[str] = None) -> List[BlogPost]:
        results = db_blogs[:limit]
        if search:
            results = [b for b in results if search.lower() in b.title.lower()]
        return results

    @staticmethod
    def get_by_id(blog_id: int) -> Optional[BlogPost]:
        return next((b for b in db_blogs if b.id == blog_id), None)

    @staticmethod
    def create(data: BlogPostCreate) -> BlogPost:
        global id_counter
        # Chuyển đổi dữ liệu từ Pydantic sang dictionary để gán ID
        # Lưu ý: Pydantic v2 dùng model_dump(), nếu bạn dùng v1 thì đổi thành dict()
        new_blog = BlogPost(id=id_counter, **data.model_dump())
        db_blogs.append(new_blog)
        id_counter += 1
        return new_blog
        
    @staticmethod
    def delete(blog_id: int) -> bool:
        global db_blogs
        blog = BlogService.get_by_id(blog_id)
        if blog:
            db_blogs = [b for b in db_blogs if b.id != blog_id]
            return True
        return False
    
    @staticmethod
    def update(blog_id: int, data: BlogPostCreate) -> Optional[BlogPost]:
        blog = BlogService.get_by_id(blog_id)
        if blog:
            # Cập nhật dữ liệu mới vào bài viết cũ
            update_data = data.model_dump()
            for key, value in update_data.items():
                setattr(blog, key, value)
            return blog
        return None