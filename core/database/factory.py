import toml
import os
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from core.database.models import Base

# dsn = os.getenv("DATABASE_URL")
# if not dsn:
#     config = toml.load('config.toml')
#     dsn = config['database']['dsn']
#
# # Исправляем postgres:// → postgresql+asyncpg://
# if dsn.startswith("postgres://"):
#     dsn = dsn.replace("postgres://", "postgresql+asyncpg://", 1)


dsn = os.getenv("DATABASE_URL")
if not dsn:
    raise RuntimeError("DATABASE_URL не установлена в переменных окружения!")

# Заменяем старый формат на async совместимый
if dsn.startswith("postgres://"):
    dsn = dsn.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(dsn, echo=True)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)





async def creat_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)