from pydantic import BaseModel, Field


class Account(BaseModel):
    number: str = Field(
        ...,
        title="Account Number (phone number)",
        regex="^01[0,1,6,7,8]{1}-\d{3,4}-\d{4}$",
    )
    password: str = Field(title="Account Password")

    class Config:
        schema_extra = {
            "example": {
                "number": "010-4234-5678",
                "password": "12341234!",
            }
        }
