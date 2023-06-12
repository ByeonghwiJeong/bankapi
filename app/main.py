import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine
from app.db import models
from app.routers import account, card
from app.auth import authentication

app = FastAPI()

app.include_router(account.router)
app.include_router(authentication.router)
app.include_router(card.router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    """
    Starts the FastAPI server.
    `poetry run uvicorn app.main:start`
    at the root of the project.
    """
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
