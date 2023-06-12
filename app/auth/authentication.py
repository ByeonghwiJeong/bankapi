from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.db.database import get_db
from app.db.models import DbAccount
from app.db.hashing import Hash
from app.auth.oauth2 import create_access_token
from app.routers.schemes import Account, OAuth2PasswordRequest


router = APIRouter(tags=["authentication"])




@router.post("/login")
def login(
    request: OAuth2PasswordRequest = Depends(), db: Session = Depends(get_db)
):
    account = db.query(DbAccount).filter(DbAccount.number == request.number).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials"
        )
    if not Hash.verify(account.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )

    access_token = create_access_token(data={"number": account.number})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "account_id": account.id,
        "number": account.number,
    }
