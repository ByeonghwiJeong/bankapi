import random
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import DbCard


def generate_card_number() -> str:
    return "-".join(["".join(random.choices("0123456789", k=4)) for _ in range(4)])


async def check_card_number_exists(db: AsyncSession, number: str) -> bool:
    # return db.query(DbCard).filter(DbCard.number == number).first() is not None
    result = await db.execute(select(DbCard).where(DbCard.number == number))
    return result.scalar_one_or_none() is not None

async def create_unique_card_number(db: AsyncSession) -> str:
    number = generate_card_number()
    while await check_card_number_exists(db, number):
        number = generate_card_number()
    return number
