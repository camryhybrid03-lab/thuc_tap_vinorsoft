# 1. Sử dụng Python 3.11 bản nhẹ
FROM python:3.11-slim

# 2. Cài đặt uv (công cụ cài thư viện siêu tốc)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Thiết lập thư mục làm việc trong container
WORKDIR /app

# 4. Copy file danh sách thư viện vào trước để cache
COPY requirements.txt ./

# 5. Cài đặt các thư viện bằng uv vào hệ thống của container
RUN uv pip install --system -r requirements.txt

# 6. Copy toàn bộ code từ folder day7 của Hiếu vào /app
COPY . .

# 7. Lệnh khởi chạy server (Lưu ý: src.main:app vì Dockerfile đang ở cùng cấp với folder src)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]