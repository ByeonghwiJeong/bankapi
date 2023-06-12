from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from app.db.models import DbAccount, DbCard, DbTransaction
from sqlalchemy.orm.session import Session
from app.db.hashing import Hash
from app.routers.schemes import AccountAuth


def authenticate_and_get_account(db: Session, request: AccountAuth, account_id: int):
    card = db.query(DbCard).filter(DbCard.number == request.number).first()
    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Card not found."
        )
    if not card.account_id == account_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    if not Hash.verify(card.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password."
        )
    account = db.query(DbAccount).filter(DbAccount.id == account_id).first()
    return account, card


def create_transaction_and_update_balance(
    db: Session,
    request: AccountAuth,
    account: DbAccount,
    card: DbCard,
    transaction_type: str,
):
    if transaction_type == "withdraw" and account.balance < request.amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance."
        )

    new_balance = (
        account.balance - request.amount
        if transaction_type == "withdraw"
        else account.balance + request.amount
    )
    account.balance = new_balance
    transaction = DbTransaction(
        amount=request.amount,
        transaction_type=transaction_type,
        card_id=card.id,
        account_id=account.id,
    )
    db.add(transaction)

    return account, card, transaction


def db_withdraw(request: AccountAuth, db: Session, account_id: int):
    account, card = authenticate_and_get_account(db, request, account_id)
    account, card, transaction = create_transaction_and_update_balance(
        db, request, account, card, "withdraw"
    )

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


def db_deposit(request: AccountAuth, db: Session, account_id: int):
    account, card = authenticate_and_get_account(db, request, account_id)
    account, card, transaction = create_transaction_and_update_balance(
        db, request, account, card, "deposit"
    )

    try:
        db.commit()
        db.refresh(account)
        db.refresh(card)
        db.refresh(transaction)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Deposit successfully.",
                "balance": account.balance,
                "transaction_id": transaction.id,
            },
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong."
        )
