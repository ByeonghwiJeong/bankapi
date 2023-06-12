from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
# from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import DbAccount, DbCard, DbTransaction
from app.db.hashing import Hash
from app.routers.schemes import AccountAuth


async def authenticate_and_get_account(db: AsyncSession, request: AccountAuth, account_id: int):
    # card = db.query(DbCard).filter(DbCard.number == request.number).first()
    query = select(DbCard).where(DbCard.number == request.number)
    result = await db.execute(query)
    card = result.scalars().first()
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
    # account = db.query(DbAccount).filter(DbAccount.id == account_id).first()
    query = select(DbAccount).where(DbAccount.id == account_id)
    result = await db.execute(query)
    account = result.scalars().first()
    return account, card


async def create_transaction_and_update_balance(
    db: AsyncSession,
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


async def db_withdraw(request: AccountAuth, db: AsyncSession, account_id: int):
    account, card = await authenticate_and_get_account(db, request, account_id)
    account, card, transaction = await create_transaction_and_update_balance(
        db, request, account, card, "withdraw"
    )

    try:
        await db.commit()
        await db.refresh(account)
        await db.refresh(card)
        await db.refresh(transaction)
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


async def db_deposit(request: AccountAuth, db: AsyncSession, account_id: int):
    account, card = await authenticate_and_get_account(db, request, account_id)
    account, card, transaction = await create_transaction_and_update_balance(
        db, request, account, card, "deposit"
    )

    try:
        await db.commit()
        await db.refresh(account)
        await db.refresh(card)
        await db.refresh(transaction)
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
