from pydantic import BaseModel, Field


class Account(BaseModel):
    username: str
    password: str = Field(title="Account Password")

    class Config:
        schema_extra = {
            "example": {
                "username": "byeonghwi",
                "password": "12341234!",
            }
        }


class AccountAuth(BaseModel):
    id: int
    username: str
    number: str


class RegisterCard(BaseModel):
    password: str = Field(
        ...,
        title="Card Password",
        regex="^\d{4}$",
    )
    class Config:
        schema_extra = {
            "example": {
                "password": "6008",
            }
        }



class Card(BaseModel):
    id: int
    number: str

    class Config:
        orm_mode = True
