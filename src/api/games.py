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
    still_open: bool
    venue: str
    odds: int


@router.get("/get_games", response_model=list[Games])
def get_games(sport: str = "all", status: str = "upcoming", page: int = 1, limit: int = 20) -> list[Games]:

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

    return result


@router.get("/game_details", response_model=Description)
def get_details(away: str, home: str):

    with db.engine.begin() as connection:
        information = connection.execute(
            sqlalchemy.text("""
                    SELECT games.location, bets.odds
                    FROM games
                    JOIN teams ON games.league_id = teams.league_id
                    JOIN bets ON bets.team_id = teams.id
                    WHERE (teams.name = :away OR teams.name = :home)AND games.date >= NOW()

                """),
            {"away": away, "home": home},
        ).first()
    if information is None:
        raise HTTPException(status_code=404, detail="Game not found")
    # {"still_open": True, "venue": information.location, "odds": information.odds}
    return Description(still_open=True, venue=information.location, odds=information.odds)
