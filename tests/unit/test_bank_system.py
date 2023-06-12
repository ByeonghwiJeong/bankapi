import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models import DbAccount
from app.db.hashing import Hash
from app.routers.account import create_account
from app.routers.schemes import Account


async def account_factory(
    session: AsyncSession, username: str, password: str, number: str
):
    """
    Helper function to create account
    """
    account = DbAccount(username=username, password=Hash.bcrypt(password), number=number)
    session.add(account)
    await session.commit()
    return account


# def card_factory(account_id):
#     """
#     Helper function to register card to a user
#     """


# @pytest.mark.asyncio
# async def test_create_user_account():
#     """
#     Test Account Creating Logic
#     """

#     #GIVEN

#     #WHEN
#         # Account Creating Logic
#     #THEN
#         # Assertion


@pytest.mark.asyncio
async def test_create_user_account(session: AsyncSession):
    """
    Test Account Creating Logic
    """

    # GIVEN
    username = "test_user"
    password = "6008"
    number = "1234567890"
    request = Account(username=username, password=password)

    # WHEN
    # with pytest.raises(HTTPException):
    #     account = await account_factory(session, username, password, number)
    #     created_account = create_account(request, session)

    # THEN
    # db_account = await session.execute(
    #     select(DbAccount).where(DbAccount.username == username)
    # )
    account = await account_factory(session, username, password, number)
    print(account)
    assert account is not None
    assert account.username == username
    assert Hash.verify(account.password, password)


# @pytest.mark.asyncio
# async def test_register_cards():

#     #GIVEN
#     _account = account_factory()

#     #WHEN
#         # Card Registration Logic
#     #THEN
#         # Assertion


# @pytest.mark.asyncio
# async def test_disable_card():
#     #GIVEN
#     _account = account_factory()
#     _card = card_factory(account_id=...)

#     #WHEN
#         # Card Disabling Logic
#     #THEN
#         #Assertion

# @pytest.mark.asyncio
# async def test_enable_card():
#     #GIVEN
#     _account = account_factory()
#     _card = card_factory(account_id=...)

#     #WHEN
#         # Card Enabling Logic

#     #THEN
#         #Assertion


# @pytest.mark.asyncio
# async def test_deposit_cash():
#     #GIVEN
#     _account = account_factory()
#     _card = card_factory(account_id=...)

#     #WHEN
#         # Money Saving Logic

#     #THEN

# @pytest.mark.asyncio
# async def test_withdraw_cash():
#     #GIVEN
#     _account = account_factory()
#     _card = card_factory(account_id=...)

#     #WHEN
#         # Money Withdrawing Logic

#     #THEN


# @pytest.mark.asyncio
# async def test_check_account_balance():
#     ...
#     #GIVEN
#     _account = account_factory()
#     _card = card_factory(account_id=...)

#     #WHEN
#         # Balace checking Logic

#     #THEN
#         #Assertion
