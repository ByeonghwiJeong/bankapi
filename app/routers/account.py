from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers.schemes import Account, AccountAuth, CardAuth
from app.db.database import get_db
from app.auth.oauth2 import get_current_account
from app.db import db_account, db_tranaction
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/account",
    tags=["account"],
)


@router.post("", response_model=Account)
async def create_account(request: Account, db: AsyncSession = Depends(get_db)):
    return await db_account.create_account(db, request)


@router.get("/{account_id}/balance")
async def get_balance(
    db: Session = Depends(get_db),
    account_id: int = None,
    current_account: AccountAuth = Depends(get_current_account),
):
    return await db_account.get_balance(db, account_id, current_account)


@router.post("/{account_id}/withdraw")
async def withdraw(
    request: CardAuth,
    db: Session = Depends(get_db),
    account_id: int = None,
):
    return await db_tranaction.db_withdraw(request, db, account_id)


@router.post("/{account_id}/deposit")
async def deposit(
    request: CardAuth,
    db: Session = Depends(get_db),
    account_id: int = None,
):
    return await db_tranaction.db_deposit(request, db, account_id)
