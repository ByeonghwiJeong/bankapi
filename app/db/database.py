from sqlalchemy.ext.asyncio import create_async_engine, async_session, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import get_db_uri


SQLALCHEMY_DATABASE_URL = get_db_uri()
print(SQLALCHEMY_DATABASE_URL)
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = async_sessionmaker(engine)

Base = declarative_base()


async def get_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()