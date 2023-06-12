from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from app.db.models import DbAccount, DbCard, DbTransaction
from app.routers.schemes import Account
from sqlalchemy.orm.session import Session
from app.db.hashing import Hash
from app.db.generate_account_num import create_unique_account_number
from app.routers.schemes import AccountAuth


def create_account(db: Session, request: Account):
    account = db.query(DbAccount).filter(DbAccount.username == request.username).first()
    if account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists."
        )
    new_account = DbAccount(
        username=request.username,
        number=create_unique_account_number(db),
        # number="11111111111",
        password=Hash.bcrypt(request.password),
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Account created successfully."},
    )


def get_account_by_username(db: Session, username: str):
    user = db.query(DbAccount).filter(DbAccount.username == username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return user


def get_balance(db: Session, account_id: int, current_account: AccountAuth):
    if account_id != current_account.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    account = get_account_by_username(db, current_account.username)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"balance": account.balance}
    )


def db_withdraw(request: AccountAuth, db: Session, account_id: int):
    card = db.query(DbCard).filter(DbCard.number == request.number).first()
    if not card.account_id == account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found."
        )
    if not Hash.verify(card.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password."
        )
    account = db.query(DbAccount).filter(DbAccount.id == account_id).first()
    if account.balance < request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient money."
        )

    account.balance -= request.amount
    transaction = DbTransaction(
        amount=request.amount,
        transaction_type="withdraw",
        card_id=card.id,
        account_id=account_id,
    )
    db.add(transaction)
    
    # transaction
    try:
        db.commit()
        db.refresh(account)
        db.refresh(card)
        db.refresh(transaction)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Withdraw successfully.",
                "balance": account.balance,
                "transaction_id": transaction.id,
            },
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong."
        )
