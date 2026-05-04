from fastapi import FastAPI
from src.api import auth

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(auth.router)
