from datetime import datetime, timedelta, timezone
from os import access, name
from typing import Annotated


from sqlalchemy.exc import IntegrityError
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from jwt import algorithms
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel


from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from sqlalchemy.engine import create
from src.api import auth
from src import database as db

from src.config import get_settings

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


class Game(BaseModel):
    id: int
    sport: str
    home_team: str
    away_team: str
    date: datetime
    location: str


class description(BaseModel):
    still_open: bool
    venue: str
    odds: int


@router.get("/get_games", response_model=list[Game])
def get_games(sport: str = "all", status: str = "upcoming", page: int = 1, limit: int = 20):

    with db.engine.begin() as connection:
        games = connection.execute(
            sqlalchemy.text("""
                SELECT games.id, leagues.sport, home_team.name, away_team.name, games.date, games.location
                FROM games
                JOIN leagues ON games.league_id = leagues.id
                JOIN teams AS home_team ON games.home_team_id = home_team.id
                JOIN teams AS away_team ON games.away_team_id = away_team.id
                WHERE (:sport = 'all' OR leagues.sport = :sport)
                """),
            {"sport": sport},
        )
        games = games.mappings().all()
    return games


@router.get("/game_details", response_model=description)
def get_details(away: str, home: str):

    with db.engine.begin() as connection:
        information = connection.execute(
            sqlalchemy.text("""
                    SELECT  location,bets.odds
                    FROM games
                    JOIN bets ON bets.game_id = games.id
                    WHERE (games.home_team_id= :home OR games.away_team_id = :away) AND games.date >= NOW()

                """),
            {"away": away, "home": home},
        ).first()
    if information is None:
        raise HTTPException(status_code=404, detail="Game not found")

    return {"still_open": True, "venue": information.location, "odds": information.odds}
