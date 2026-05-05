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
    date: datetime
    location: str


class Description(BaseModel):
    game_id: int
    league_id: int
    home_team: str
    away_team: str
    date: datetime
    location: str
    home_odds: float
    away_odds: float


@router.get("/get_games", response_model=list[Games])
def get_games(
    sport: str = "all", status: str = "upcoming", page: int = 1, limit: int = 20
) -> list[Games]:

    with db.engine.begin() as connection:
        rows = (
            connection.execute(
                sqlalchemy.text("""
                SELECT
                    games.id,
                    leagues.sport,
                    home_team.name AS home_team,
                    away_team.name AS away_team,
                    games.date,
                    games.location
                FROM games
                JOIN leagues ON games.league_id = leagues.id
                JOIN teams AS home_team ON games.home_team_id = home_team.id
                JOIN teams AS away_team ON games.away_team_id = away_team.id
                WHERE (:sport = 'all' OR leagues.sport = :sport)

            """),
                {"sport": sport},
            )
            .mappings()
            .all()
        )
    result = []
    for game in rows:
        result.append(
            Games(
                id=game["id"],
                sport=game["sport"],
                home_team=game["home_team"],
                away_team=game["away_team"],
                date=game["date"],
                location=game["location"],
            )
        )

    if result == []:
        raise HTTPException(status_code=404, detail="Games Not Found / Bad Input")
    return result


@router.get("/game_details", response_model=Description)
def get_details(id: int):

    with db.engine.begin() as connection:
        info = connection.execute(
            sqlalchemy.text("""
                SELECT games.id as id, games.league_id as league_id, hteam.name AS home, ateam.name as away, date, games.location as location, home_odds, away_odds 
                FROM games
                JOIN teams AS hteam
                    ON hteam.id = games.home_team_id
                JOIN teams AS ateam
                    ON ateam.id = games.away_team_id
                WHERE games.id = :id;
                """),
            {"id": id},
        ).first()
    if info is None:
        raise HTTPException(status_code=404, detail="Game not found")

    print(info)
    return Description(
        game_id=info.id,
        league_id=info.league_id,
        home_team=info.home,
        away_team=info.away,
        date=info.date,
        location=info.location,
        home_odds=info.home_odds,
        away_odds=info.away_odds,
    )
