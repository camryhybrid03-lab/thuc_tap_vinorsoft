from fastapi import FastAPI
from src.api.blog_router import router as blog_router

app = FastAPI(
    title="Personal Blog API",
    description="API quản lý Blog cá nhân chuẩn cấu trúc Enterprise - Day 4",
    version="2.0.0"
)

# Gắn toàn bộ các API con (router) vào app chính
app.include_router(blog_router)

@app.get("/", tags=["Trang chủ"])
def home():
    return {
        "message": "Hệ thống API đang chạy!",
        "docs": "Truy cập http://127.0.0.1:8000/docs để xem tài liệu API"
    }