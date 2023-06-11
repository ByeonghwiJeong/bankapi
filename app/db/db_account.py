from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from app.db.models import DbAccount
from app.routers.schemes import Account
from sqlalchemy.orm.session import Session
from app.db.hashing import Hash

def create_account(db: Session, request: Account):
    account = db.query(DbAccount).filter(DbAccount.number == request.number).first()
    if account:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists.")
    new_account = DbAccount(
        number=request.number,
        password=Hash.bcrypt(request.password),
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Account created successfully."})


