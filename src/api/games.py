from datetime import date, datetime
from enum import Enum
from typing import Sequence
import sqlalchemy
from fastapi import APIRouter, Depends, HTTPException, Response
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


class SearchResponse(BaseModel):
    page: int
    limit: int
    total: int
    games: list[Games]


class League(str, Enum):
    MLB = "mlb"
    WORLD_CUP = "world_cup"


class Status(str, Enum):
    upcoming = "upcoming"
    live = "live"
    finished = "finished"


@router.get("/", response_model=SearchResponse)
def get_games(
    league: League = League.NLB,
    status: Status = Status.upcoming,
    page: int = 1,
    limit: int = 20,
) -> SearchResponse:

    if page < 1:
        raise HTTPException(status_code=400, detail="Page number cannot be less than 1")

    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit cannot be 0 or negative")
    elif limit > 100:
        raise HTTPException(status_code=400, detail="Limit cannot be over 100")

    offset = (page - 1) * limit

    if status == "upcoming":
        interval = "NOW() < games.date"

    elif status == "live":
        interval = "NOW() < games.date + INTERVAL '2 hours' AND games.date <= NOW()"

    else:
        interval = "games.date + INTERVAL '2 hours' <= NOW()"

    with db.engine.begin() as connection:
        games = connection.execute(
            sqlalchemy.text(f"""
                SELECT * FROM (
                    SELECT
                        games.id,
                        leagues.sport,
                        home_team.name AS home_team,
                        away_team.name AS away_team,
                        games.date,
                        games.location,
                        :status AS status
                    FROM games
                    JOIN leagues ON games.league_id = leagues.id
                    JOIN teams AS home_team ON games.home_team_id = home_team.id
                    JOIN teams AS away_team ON games.away_team_id = away_team.id
                    WHERE leagues.name = :league AND {interval}
                ) AS subquery
                WHERE status = :status
                ORDER BY date ASC
                OFFSET :offset
                LIMIT :limit

            """),
            {"league": league, "status": status, "offset": offset, "limit": limit},
        )

    total = games.rowcount

    games = games.mappings().all()

    if not games:
        raise HTTPException(status_code=404, detail="Games Not Found / Bad Input")

    return SearchResponse(page=page, limit=limit, total=total, games=map_games(games))


@router.get("/{game_id}", response_model=Description)
def get_details(game_id: int):

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
            {"id": game_id},
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


@router.post("/{game_id}/comments", response_model=Post_Comment_Response)
def post_comment(
    body: str,
    game_id: int,
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
):
    profanity = ["bitch", "fuck"]

    if not body:
        raise HTTPException(
            status_code=400,
            detail={"error_code": "INVALID_COMMENT", "message": "Body cannot be empty"},
        )
    with db.engine.begin() as connection:

        recent_comments = connection.execute(
            sqlalchemy.text("""
            SELECT COUNT(*)
            FROM comments
            WHERE user_id = :user_id
            AND posted_at >= NOW() - INTERVAL '2 minute'
        """),
            {"user_id": current_token_data.user_id},
        ).scalar()

        if recent_comments != None:
            if recent_comments >= 5:
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error_code": "RATE_LIMIT_EXCEEDED",
                        "message": "Too many comments. Please wait before posting again.",
                    },
                )

        words_body = body.split(" ")

        for words in profanity:
            for word in words_body:
                if word == words:
                    raise HTTPException(
                        status_code=400,
                        detail="All or Nothing does not support profanity :)",
                    )

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


class Comment(BaseModel):
    comment_id: int
    user_id: int
    username: str
    body: str
    posted_at: datetime


def map_comments(comments: Sequence[RowMapping]) -> list[Comment]:
    return [
        Comment(
            comment_id=comment["comment_id"],
            user_id=comment["user_id"],
            username=comment["username"],
            body=comment["body"],
            posted_at=comment["posted_at"],
        )
        for comment in comments
    ]


@router.get("/{game_id}/comments", response_model=list[Comment])
def get_comments(
    game_id: int,
    page: int = 1,
    limit: int = 20,
) -> list[Comment]:
    offset = (page - 1) * limit
    with db.engine.begin() as connection:
        comments = (
            connection.execute(
                sqlalchemy.text("""
            SELECT c.id AS comment_id, c.user_id, u.name AS username, c.body, c.posted_at
            FROM games
            JOIN "comments" c ON c.game_id = games.id
            JOIN users u  ON c.user_id = u.id
            WHERE games.id = :game_id
            ORDER BY c.posted_at ASC
            OFFSET :offset
            LIMIT :limit
        """),
                {"game_id": game_id, "offset": offset, "limit": limit},
            )
            .mappings()
            .all()
        )

        if not comments:
            game = connection.execute(
                sqlalchemy.text("""
                SELECT id FROM games WHERE id = :game_id
            """),
                {"game_id": game_id},
            ).fetchone()

            if game is None:
                raise HTTPException(status_code=404, detail="Game not found")
            return []

    return map_comments(comments)


@router.delete("/{game_id}/comments/{comment_id}", response_class=Response)
def delete_comment(
    game_id: int,
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
    comment_id: int,
):
    with db.engine.begin() as connection:
        comment_user_id = connection.execute(
            sqlalchemy.text("""
            SELECT user_id
            FROM comments
            WHERE id = :comment_id AND game_id = :game_id
            """),
            {"comment_id": comment_id, "game_id": game_id},
        ).scalar_one_or_none()
        if not comment_user_id:
            raise HTTPException(status_code=404, detail="Comment does not exist")
        if comment_user_id != current_token_data.user_id:
            raise HTTPException(
                status_code=403, detail="You can only delete your comments"
            )
        result = connection.execute(
            sqlalchemy.text("""
                DELETE FROM comments
                WHERE id = :comment_id
                """),
            {"comment_id": comment_id},
        )
        if not result.rowcount:
            raise HTTPException(status_code=404, detail="Error deleting comment...")
    return Response(status_code=204)
