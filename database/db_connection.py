from sqlalchemy.orm import sessionmaker

from .config import DB_PORT, DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base


DB_CONNECTION_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DB_CONNECTION_URL, echo=True) # False for production

Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession: # depends
    async with async_session() as session:
        yield session

async def init_models() -> None: # Создание таблиц
    async with engine.begin() as conn:
        if not (await conn.run_sync(engine.dialect.has_table, "employees")) or \
           not (await conn.run_sync(engine.dialect.has_table, "subdivisions")) or \
           not (await conn.run_sync(engine.dialect.has_table, "business_trip_schedules")) or \
           not (await conn.run_sync(engine.dialect.has_table, "vacation_schedules")):
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print("YES")
