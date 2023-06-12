from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.db.models import DbCard
from app.routers.schemes import AccountAuth, RegisterCard, UpdateCard
from sqlalchemy.orm.session import Session
from app.db.hashing import Hash
from app.db.generate_card import create_unique_card_number
from app.db.state_card import Card


def register_card(db: Session, request: RegisterCard, current_account: AccountAuth):
    new_card = DbCard(
        number=create_unique_card_number(db),
        password=Hash.bcrypt(request.password),
        account_id=current_account.id,
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={"message": "Card registered successfully.", "card_number": new_card.number},
    )


def update_card_activation(db: Session, request: UpdateCard, current_account: AccountAuth):
    card = db.query(DbCard).filter(DbCard.number == request.number).first()
    if (not card) or (card.account_id != current_account.id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="you are not authorized to perform this action.",
        )
    if not Hash.verify(card.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect password"
        )
    print("before active", card.is_active)
    is_active = Card(card.is_active)
    is_active.change()
    print("after active", is_active.status())
    card.is_active = is_active.status()
    db.commit()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Card Status updated to {'Enabled' if is_active.status() else 'Disabled'} successfully."
        },
    )
