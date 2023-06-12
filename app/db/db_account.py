from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from app.db.models import DbAccount
from app.routers.schemes import Account
from sqlalchemy.orm.session import Session
from app.db.hashing import Hash
from app.db.generate_account_num import create_unique_account_number
from app.routers.schemes import AccountAuth


def create_account(db: Session, request: Account):
    account = db.query(DbAccount).filter(DbAccount.username == request.username).first()
    if account:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists.")
    new_account = DbAccount(
        username=request.username,
        number=create_unique_account_number(db),
        # number="11111111111",
        password=Hash.bcrypt(request.password),
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Account created successfully."})


def get_account_by_username(db: Session, username: str):
  user = db.query(DbAccount).filter(DbAccount.username == username).first()
  if not user:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
      detail=f'User with username {username} not found')
  return user


def get_balance(db: Session, account_id: int, current_account: AccountAuth):
    if account_id != current_account.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    account = get_account_by_username(db, current_account.username)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"balance": account.balance})