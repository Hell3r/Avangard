from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool
import os
from src.models import *
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://evgeniy:postgres@localhost:5432/avangard")


engine = create_async_engine(
    DATABASE_URL,
    echo=True, 
    pool_pre_ping=True,  
    pool_size=5,  
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)



async def get_session():
    async with new_async_session() as session:
        yield session
        
class Base(DeclarativeBase):
    pass