# from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from app.routers.schemes import Account
from app.db.database import get_db
from app.db import db_card
from app.auth.oauth2 import get_current_account
from app.routers.schemes import AccountAuth, UpdateCard, RegisterCard


router = APIRouter(
    prefix="/card",
    tags=["card"],
)


@router.post("")
async def register_card(
    request: RegisterCard,
    db: AsyncSession = Depends(get_db),
    current_account: AccountAuth = Depends(get_current_account),
):
    return await db_card.register_card(db, request, current_account)


@router.put("")
async def update_active_card(
    request: UpdateCard,
    db: AsyncSession = Depends(get_db),
    current_account: AccountAuth = Depends(get_current_account),
):
    return await db_card.update_card_activation(db, request, current_account)
