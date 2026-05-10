from fastapi import FastAPI
from src.api import auth, games, bets, leaderboard

tags_metadata = [
    {"name": "bets", "description": "make some money"},
]

app = FastAPI(
    title="All Or Nothing",
    description="Website like prizepicks",
    version="1.0",
    openapi_tags=tags_metadata,
)

app.include_router(bets.router)


@app.get("/")
def root():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(games.router)
app.include_router(leaderboard.router)
