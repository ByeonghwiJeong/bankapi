from fastapi import status
from fastapi.responses import JSONResponse
from app.db.models import DbCard
from app.routers.schemes import AccountAuth, RegisterCard
from sqlalchemy.orm.session import Session
from app.db.hashing import Hash
from app.db.generate_card import create_unique_card_number


def register_card(db: Session, request: RegisterCard, current_account: AccountAuth):
    new_card = DbCard(
        number=create_unique_card_number(db),
        password=Hash.bcrypt(request.password),
        account_id=current_account.id,
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Card registered successfully."})


