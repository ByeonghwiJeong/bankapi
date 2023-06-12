import random
from sqlalchemy.orm import Session
from app.db.models import DbAccount


def generate_account_number() -> str:
    return "".join(random.choices("0123456789", k=12))


def check_account_number_exists(db: Session, number: str) -> bool:
    print("dbdbdbdbdbdb Check")
    return db.query(DbAccount).filter(DbAccount.number == number).first() is not None


def create_unique_account_number(db: Session) -> str:
    number = generate_account_number()
    while check_account_number_exists(db, number):
        number = generate_account_number()
    return number
