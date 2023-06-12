from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
# from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import DbAccount, DbCard, DbTransaction
from app.routers.schemes import Account
from app.db.hashing import Hash
from app.db.generate_account_num import create_unique_account_number
from app.routers.schemes import AccountAuth


async def create_account(db: AsyncSession, request: Account):
    # account = db.query(DbAccount).filter(DbAccount.username == request.username).first()
    query = select(DbAccount).where(DbAccount.username == request.username)
    result = await db.execute(query)
    account = result.scalars().first()

    if account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="username already exists."
        )
    new_account = DbAccount(
        username=request.username,
        number=await create_unique_account_number(db),
        password=Hash.bcrypt(request.password),
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Account created successfully."},
    )


async def get_account_by_username(db: AsyncSession, username: str):
    # user = db.query(DbAccount).filter(DbAccount.username == username).first()
    query = select(DbAccount).where(DbAccount.username == username)
    result = await db.execute(query)
    account = result.scalars().first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with username {username} not found",
        )
    return account


async def get_balance(db: AsyncSession, account_id: int, current_account: AccountAuth):
    if account_id != current_account.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    account = await get_account_by_username(db, current_account.username)
    return JSONResponse(
        status_code=status.HTTP_200_OK, content={"balance": account.balance}
    )
