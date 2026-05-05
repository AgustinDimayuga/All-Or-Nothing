from fastapi import FastAPI
from src.api import auth, games

app = FastAPI()


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(games.router)
