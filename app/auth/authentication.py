from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.db.database import get_db
from app.db.models import DbAccount
from app.db.hashing import Hash
from app.auth.oauth2 import create_access_token


router = APIRouter(tags=["authentication"])


@router.post("/login")
def login(
    request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    account = db.query(DbAccount).filter(DbAccount.username == request.username).first()
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
