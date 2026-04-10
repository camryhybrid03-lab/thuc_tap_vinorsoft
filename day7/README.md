🚀 FastAPI Learning Journey - Day 7

Dự án này đánh dấu cột mốc quan trọng trong việc chuyển đổi sang môi trường Docker hóa hoàn chỉnh.

📌 Tính năng chính

Dockerize: Đóng gói FastAPI và Postgres vào container.

PostgreSQL: Sử dụng database chuyên nghiệp thay cho SQLite.

Async SQLAlchemy: Xử lý database bất đồng bộ.

🚀 Cách khởi chạy hệ thống

1. Yêu cầu hệ thống

Máy đã cài sẵn Docker và Docker Desktop.

2. Chạy ứng dụng

Mở Terminal tại thư mục gốc và gõ:

docker-compose up --build


3. Truy cập Swagger UI

Sau khi hệ thống khởi động thành công, truy cập các đường dẫn sau để test API:

API Documentation: http://localhost:8000/docs

Alternative Docs: http://localhost:8000/redoc

🐳 Các lệnh Docker hữu ích đã học

Dưới đây là các lệnh quan trọng để quản lý hệ thống:

# Chạy hệ thống (không build lại)
docker-compose up

# Dừng hệ thống
docker-compose down

# Xóa sạch container và dữ liệu (Reset sạch sẽ)
docker-compose down -v

# Truy cập trực tiếp vào DB để kiểm tra (Thay user và db_name tương ứng)
docker exec -it <container_name> psql -U <username> -d <database_name>
