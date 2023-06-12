import random
from sqlalchemy.orm import Session
from app.db.models import DbCard

def generate_card_number() -> str:
    return '-'.join([''.join(random.choices('0123456789', k=4)) for _ in range(4)])

def check_card_number_exists(db: Session, number: str) -> bool:
    return db.query(DbCard).filter(DbCard.number == number).first() is not None

def create_unique_card_number(db: Session) -> str:
    number = generate_card_number()
    while check_card_number_exists(db, number):
        number = generate_card_number()
    return number
