from enum import Enum
from typing import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
import sqlalchemy
from src.api.user_helper import *
from src import database as db

router = APIRouter(
    prefix="/users", tags=["user"], dependencies=[Depends(get_token_data)]
)


class Active_bets(BaseModel):
    team: str
    wagered: float
    potential: float


class Balance(BaseModel):
    balance: float


@router.get("/balance", response_model=Balance)
def get_balance(current_token_data: Annotated[TokenData, Depends(get_token_data)]):

    with db.engine.begin() as connection:
        money = connection.execute(
            sqlalchemy.text("""
            SELECT COALESCE(SUM(change),0) AS balance
            FROM wallet
            WHERE wallet.user_id = :id

            """),
            {"id": current_token_data.user_id},
        ).scalar_one()
    if money == None:
        raise HTTPException(status_code=404, detail="Could not find Wallet")

    return Balance(balance=money)


@router.get("/me/")
async def read_users_me(
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
) -> TokenData:
    return current_token_data


class BetStatus(str, Enum):
    won = "won"
    lost = "lost"
    pending = "pending"
    all = "all"


class UserBet(BaseModel):
    bet_id: int
    game_id: int
    team_id: int
    team_bet_on: str
    amount: float
    odds: float
    potential_payout: float
    status: BetStatus
    placed_at: datetime


class TotalUserBets(BaseModel):
    user_id: int
    status: BetStatus
    page: int
    limit: int
    total: int
    returned: int
    bets: list[UserBet]

@router.get("/withdraw")
def withdraw_money(user_id: int , amount: float ):

    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text("""
                INSERT INTO wallet (change)
                """))


@router.get("/me/bets", response_model=TotalUserBets)
def get_user_bets(
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
    status: BetStatus = BetStatus.all,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
) -> TotalUserBets:
    offset = (page - 1) * limit

    if status == BetStatus.won:
        status_filter = "AND bets.resolved = true AND games.result IS NOT NULL AND bets.team_id = games.result"
    elif status == BetStatus.lost:
        status_filter = "AND bets.resolved = true AND games.result IS NOT NULL AND bets.team_id != games.result"
    elif status == BetStatus.pending:
        status_filter = "AND bets.resolved = false"
    else:  # all
        status_filter = ""

    with db.engine.begin() as connection:
        total = connection.execute(
            sqlalchemy.text(f"""
                SELECT COUNT(*)
                FROM bets
                JOIN games ON bets.game_id = games.id
                WHERE bets.user_id = :user_id
                  {status_filter}
            """),
            {"user_id": current_token_data.user_id},
        ).scalar_one()

        bets = (
            connection.execute(
                sqlalchemy.text(f"""
                SELECT
                    bets.id,
                    bets.game_id,
                    bets.team_id,
                    teams.name,
                    bets.amount,
                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds
                    END AS odds,
                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds * bets.amount
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds * bets.amount
                    END AS potential_payout,
                    bets.created_at,
                    games.result
                FROM bets
                JOIN games ON bets.game_id = games.id
                JOIN teams ON bets.team_id = teams.id
                WHERE bets.user_id = :user_id
                  {status_filter}
                ORDER BY bets.created_at DESC
                LIMIT :limit OFFSET :offset
                """),
                {
                    "user_id": current_token_data.user_id,
                    "limit": limit,
                    "offset": offset,
                },
            )
            .mappings()
            .all()
        )

    bets_list = [
        UserBet(
            bet_id=bet["id"],
            game_id=bet["game_id"],
            team_id=bet["team_id"],
            team_bet_on=bet["name"],
            amount=bet["amount"],
            odds=bet["odds"],
            potential_payout=bet["potential_payout"],
            status=(
                BetStatus.won
                if bet["result"] == bet["team_id"]
                else BetStatus.lost if bet["result"] is not None else BetStatus.pending
            ),
            placed_at=bet["created_at"],
        )
        for bet in bets
    ]

    return TotalUserBets(
        user_id=current_token_data.user_id,
        status=status,
        page=page,
        limit=limit,
        total=total,
        returned=len(bets_list),
        bets=bets_list,
    )
