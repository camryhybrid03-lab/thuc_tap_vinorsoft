from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Dùng SQLite để test cho nhanh, file db sẽ tên là sql_app.db
# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./sql_app.db"

# Cấu trúc: postgresql+asyncpg://[user]:[password]@[host]:[port]/[db_name]

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres@localhost:5432/blog_fastapi"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Hàm lấy session để các API sử dụng
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session