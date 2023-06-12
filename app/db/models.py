from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, Boolean, BigInteger, DateTime, Enum
from sqlalchemy import Column
from sqlalchemy.sql import func
from app.db.database import Base


class DbAccount(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    number = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    limit = Column(Integer, default=0)
    balance = Column(BigInteger, default=0)
    cards = relationship("DbCard", back_populates="account")
    transactions = relationship("DbTransaction", back_populates="account")


class DbCard(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("DbAccount", back_populates="cards")
    transactions = relationship("DbTransaction", back_populates="card")

class TransactionType(PyEnum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"


class DbTransaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    card_id = Column(Integer, ForeignKey("cards.id"))
    card = relationship("DbCard", back_populates="transactions")
    account_id = Column(Integer, ForeignKey("accounts.id"))
    account = relationship("DbAccount", back_populates="transactions")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
