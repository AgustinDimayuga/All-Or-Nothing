from datetime import datetime
import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db

router = APIRouter(
    prefix="/games",
    tags=["games"],
)


class Games(BaseModel):
    id: int
    sport: str
    home_team: str
    away_team: str
    date: str
    location: str


class Description(BaseModel):
    still_open: bool
    venue: str
    odds: int


@router.get("/get_games", response_model=list[Games])
def get_games(
    sport: str = "all", status: str = "upcoming", page: int = 1, limit: int = 20
) -> list[Games]:

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

    return [
        Games(
            id=1,
            sport="hello",
            home_team="home",
            away_team="away",
            date="date",
            location="locations",
        )
    ]


@router.get("/game_details", response_model=Description)
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
