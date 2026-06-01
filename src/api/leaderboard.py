from datetime import datetime
import sqlalchemy
from fastapi import APIRouter, Query
from pydantic import BaseModel
from enum import Enum
from src import database as db
import time

router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
)


class Period(str, Enum):
    daily = "daily"
    weekly = "weekly"


class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    net_earnings: float


class Leaderboard(BaseModel):
    period: Period
    limit: int
    leaderboard: list[LeaderboardEntry]


@router.get("/", response_model=Leaderboard)
def get_leaderboard(
    period: Period = Period.weekly,
    limit: int = Query(default=25, ge=1, le=100),
) -> Leaderboard:
    # start = time.perf_counter() 

    interval = "7 days" if period == Period.weekly else "1 day"

    with db.engine.begin() as connection:
        users = (
            connection.execute(
                sqlalchemy.text("""
                    SELECT
                        users.id,
                        users.username,
                        COALESCE(SUM(wallet.change), 0) AS net_earnings
                    FROM users
                    JOIN wallet ON users.id = wallet.user_id
                    JOIN bets ON wallet.from_bet = bets.id
                    WHERE wallet.from_bet IS NOT NULL
                      AND bets.created_at >= NOW() - CAST(:interval AS INTERVAL)
                    GROUP BY users.id, users.username
                    ORDER BY net_earnings DESC
                    LIMIT :limit
                """),
                {"interval": interval, "limit": limit},
            )
            .mappings()
            .all()
        )

    leaderboard = [
        LeaderboardEntry(
            rank=i + 1,
            user_id=user["id"],
            username=user["username"],
            net_earnings=float(user["net_earnings"]),
        )
        for i, user in enumerate(users)
    ]
    # elapsed_ms = (time.perf_counter() - start) * 1000
    # print(f"{elapsed_ms:.2f}" + " ms")
    return Leaderboard(
        period=period,
        limit=limit,
        leaderboard=leaderboard,
    )
