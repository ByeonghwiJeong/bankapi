from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.db.models import DbAccount
from app.db.hashing import Hash
from app.auth.oauth2 import create_access_token


router = APIRouter(tags=["authentication"])


@router.post("/login")
async def login(
    request: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    query = select(DbAccount).where(DbAccount.username == request.username)
    result = await db.execute(query)
    account = result.scalars().first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify(account.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    access_token = create_access_token(data={"username": account.username})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "account_id": account.id,
        "username": account.username,
    }
