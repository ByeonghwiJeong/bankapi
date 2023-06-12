from sqlalchemy.orm.session import Session
from app.routers.schemes import Account, AccountAuth
from app.db.database import get_db
from app.auth.oauth2 import get_current_account
from app.db import db_account
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/account",
    tags=["account"],
)


@router.post("", response_model=Account)
async def create_account(request: Account, db: Session = Depends(get_db)):
    return db_account.create_account(db, request)


@router.get("/balance")
async def get_balance(
    db: Session = Depends(get_db),
    current_account: AccountAuth = Depends(get_current_account),
):
    return db_account.get_balance(db, current_account)
