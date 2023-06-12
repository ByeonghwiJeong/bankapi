import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import DbAccount


def generate_account_number() -> str:
    return "".join(random.choices("0123456789", k=12))


async def check_account_number_exists(db: AsyncSession, number: str) -> bool:
    result = await db.execute(select(DbAccount).where(DbAccount.number == number))
    return result.scalar_one_or_none() is not None


async def create_unique_account_number(db: AsyncSession) -> str:
    number = generate_account_number()
    while await check_account_number_exists(db, number):
        number = generate_account_number()
    return number
