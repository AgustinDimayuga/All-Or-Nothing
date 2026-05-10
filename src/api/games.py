from datetime import datetime
from enum import Enum
from typing import Sequence
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import RowMapping
from src import database as db
from src.api.user_helper import get_token_data, TokenData

from typing import Annotated

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


def map_games(games: Sequence[RowMapping]):
    return [
        Games(
            id=game["id"],
            sport=game["sport"],
            home_team=game["home_team"],
            away_team=game["away_team"],
            date=game["date"],
            location=game["location"],
        )
        for game in games
    ]


class League(str, Enum):
    NBA = "nba"
    MLS = "mls"
    NHL = "nhl"


class Status(str, Enum):
    upcoming = "upcoming"
    live = "live"
    finished = "finished"


@router.get("/games", response_model=list[Games])
def get_games(
    league: League,
    status: Status,
    page: int = 1,
    limit: int = 20,
) -> list[Games]:
    offset = (page - 1) * limit

    with db.engine.begin() as connection:
        games = (
            connection.execute(
                sqlalchemy.text("""
                SELECT * FROM (
                    SELECT
                        games.id,
                        leagues.sport,
                        home_team.name AS home_team,
                        away_team.name AS away_team,
                        games.date,
                        games.location,
                        CASE
                            WHEN NOW() < date THEN 'upcoming'
                            WHEN NOW() < date + INTERVAL '2 hours' THEN 'live'
                            ELSE 'finished'
                        END AS status
                    FROM games
                    JOIN leagues ON games.league_id = leagues.id
                    JOIN teams AS home_team ON games.home_team_id = home_team.id
                    JOIN teams AS away_team ON games.away_team_id = away_team.id
                    WHERE leagues.name = :league
                ) AS subquery
                WHERE status = :status
                OFFSET :offset
                LIMIT :limit

            """),
                {"league": league, "status": status, "offset": offset, "limit": limit},
            )
            .mappings()
            .all()
        )

    if not games:
        raise HTTPException(status_code=404, detail="Games Not Found / Bad Input")
    return map_games(games)


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


class Post_Comment_Response(BaseModel):
    comment_id: int
    posted_at: datetime
    body: str


@router.post("/{game_od}/comments", response_model=Post_Comment_Response)
def post_comment(
    body: str,
    game_id: int,
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
):

    if not body:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "INVALID_COMMENT", "message": "Body cannot be empty"},
        )
    with db.engine.begin() as connection:
        comment = connection.execute(
            sqlalchemy.text("""
            INSERT INTO COMMENTS (user_id,body,game_id)
            VALUES (:user_id, :body,:game_id)
            RETURNING id, body, posted_at
            """),
            {"user_id": current_token_data.user_id, "body": body, "game_id": game_id},
        ).one()
    return Post_Comment_Response(
        comment_id=comment.id, posted_at=comment.posted_at, body=comment.body
    )
