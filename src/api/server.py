from fastapi import FastAPI
from src.api import bets

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
