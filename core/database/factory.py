import os

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from core.database.models import Base

from config import Config

config = Config.from_file("config.toml")


engine = create_async_engine(config.database.dsn, echo=True)
session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)


async def creat_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)