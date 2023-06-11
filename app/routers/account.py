from sqlalchemy.orm.session import Session
from app.routers.schemes import Account
from app.db.database import get_db
from app.db import db_account
from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/account",
    tags=["account"],
)

@router.post("", response_model=Account)
async def create_account(request: Account, db: Session = Depends(get_db)):
    return db_account.create_account(db, request)
