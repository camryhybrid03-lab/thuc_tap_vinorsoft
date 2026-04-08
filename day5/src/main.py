from fastapi import FastAPI
# Import cái router mà bạn vừa tạo ở bước trước
from src.api.blog_router import router as blog_router

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="Blog System - Day 5",
    description="Hệ thống Blog sử dụng FastAPI, SQLAlchemy và PostgreSQL/SQLite",
    version="1.0.0"
)

# Đấu nối Router vào App chính
# Tất cả các API trong blog_router sẽ được gắn vào app này
app.include_router(blog_router)

# Thêm một trang chào mừng đơn giản để kiểm tra xem server có chạy không
@app.get("/")
async def root():
    return {
        "message": "Chào Hiếu! Server Day 5 đã online.",
        "status": "success",
        "docs": "/docs"
    }