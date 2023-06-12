from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# from sqlalchemy.orm.session import Session
from app.db.models import DbCard
from app.routers.schemes import AccountAuth, RegisterCard, UpdateCard
from app.db.hashing import Hash
from app.db.generate_card import create_unique_card_number
from app.db.state_card import Card


async def register_card(db: AsyncSession, request: RegisterCard, current_account: AccountAuth):
    new_card = DbCard(
        number=await create_unique_card_number(db),
        password=Hash.bcrypt(request.password),
        account_id=current_account.id,
    )
    db.add(new_card)
    await db.commit()
    await db.refresh(new_card)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "message": "Card registered successfully.",
            "card_number": new_card.number,
        },
    )


async def update_card_activation(
    db: AsyncSession, request: UpdateCard, current_account: AccountAuth
):
    # card = db.query(DbCard).filter(DbCard.number == request.number).first()
    query = select(DbCard).where(DbCard.number == request.number)
    result = await db.execute(query)
    card = result.scalars().first()
    if (not card) or (card.account_id != current_account.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    if not Hash.verify(card.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    is_active = Card(card.is_active)
    is_active.change()
    card.is_active = is_active.status()
    await db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Card Status updated to {'Enabled' if is_active.status() else 'Disabled'} successfully."
        },
    )
