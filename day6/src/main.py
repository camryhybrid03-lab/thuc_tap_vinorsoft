from fastapi import FastAPI
# 1. Sửa lại cách import cho đồng nhất
from src.api.blog_router import router as blog_router
from src.api.user_router import router as user_router 

app = FastAPI(
    title="Blog System - Day 6", # Cập nhật lên Day 6 luôn cho máu
    description="Hệ thống Blog có thêm chức năng User và Authentication",
    version="1.0.0"
)

# 2. Đấu nối Router (Gọi trực tiếp tên đã alias)
app.include_router(blog_router)
app.include_router(user_router) # Không cần .router nữa vì mình đã import đích danh nó rồi

@app.get("/")
async def root():
    return {
        "message": "Chào Hiếu! Hệ thống User Day 6 đã sẵn sàng.",
        "status": "success",
        "docs": "/docs"
    }