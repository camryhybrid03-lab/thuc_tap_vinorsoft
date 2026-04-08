from fastapi import FastAPI
from src.database import engine
# SỬA Ở ĐÂY: Import Base từ models để nó mang theo BlogDB và User
from src.models import Base 
from src.api.blog_router import router as blog_router
from src.api.user_router import router as user_router 

app = FastAPI(
    title="Blog System - Day 7",
    description="Hệ thống Blog chạy trên Docker với tính năng tự động tạo bảng",
    version="1.0.0"
)

# --- TỰ ĐỘNG TẠO BẢNG ---
@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        # Lệnh này sẽ tạo tất cả bảng đã import vào file models/__init__.py
        await conn.run_sync(Base.metadata.create_all)
    print("--- [DOCKER] DATABASE TABLES CREATED SUCCESSFULLY ---")

app.include_router(blog_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": "Chào Hiếu! Hệ thống Day 7 đã sẵn sàng.",
        "status": "success"
    }