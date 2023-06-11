import uvicorn
from fastapi import FastAPI


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


def start():
    """Starts the FastAPI server. `poetry run uvicorn app.main:start` at the root of the project."""
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)