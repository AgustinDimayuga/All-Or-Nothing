from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Annotated
from datetime import datetime


import sqlalchemy
from src.api.user_helper import get_token_data, TokenData
from src import database as db

router = APIRouter(
    prefix="/bets", tags=["bets"], dependencies=[Depends(get_token_data)]
)


class Bet(BaseModel):
    game_id: int
    team: str
    amount: float


class BetResponse(BaseModel):
    bet_id: int
    game_id: int
    team_bet_on: str
    amount: float
    odds: float
    potential_payout: float
    status: str
    placed_at: str
    new_balance: float


@router.post("/", response_model=BetResponse)
def place_bet(
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
    new_bet: Bet,
):

    user_id = current_token_data.user_id

    if new_bet.amount <= 0:
        raise HTTPException(
            status_code=400, detail="bet amount cannot be 0 or negative"
        )

    with db.engine.begin() as connection:

        cur_balance = connection.execute(
            sqlalchemy.text("""
                SELECT sum(change)
                FROM wallet
                WHERE user_id = :user_id
                """),
            [{"user_id": user_id}],
        ).scalar_one()

        if new_bet.amount > cur_balance:
            raise HTTPException(status_code=422, detail="Not enough money")

        get_odds = (
            connection.execute(
                sqlalchemy.text("""
                SELECT * 
                FROM (SELECT home_team_id, away_team_id, home_odds, away_odds, teams.id AS team_id,      
                        CASE
                            WHEN NOW() < date THEN 'upcoming'
                            WHEN NOW() < date + INTERVAL '2 hours' THEN 'live'
                            ELSE 'finished'
                        END AS status
                FROM games
                JOIN teams ON teams.id = games.home_team_id OR teams.id = games.away_team_id
                WHERE games.id = :game_id AND teams.name = :team_name ) WHERE status = 'upcoming'
                """),
                [{"game_id": new_bet.game_id, "team_name": new_bet.team}],
            )
            .mappings()
            .one_or_none()
        )

        if not get_odds:
            raise HTTPException(
                status_code=400,
                detail="Team is not playing or Game Already Started",
            )

        team_id = get_odds["team_id"]

        if team_id == get_odds["home_team_id"]:
            odds = get_odds["home_odds"]
        elif team_id == get_odds["away_team_id"]:
            odds = get_odds["away_odds"]

        values = (
            connection.execute(
                sqlalchemy.text("""
                INSERT INTO bets (user_id, game_id, team_id, amount)
                VALUES (:user_id, :game_id, :team_id, :amount)
                RETURNING id, created_at
                """),
                [
                    {
                        "user_id": user_id,
                        "game_id": new_bet.game_id,
                        "team_id": team_id,
                        "amount": new_bet.amount,
                    }
                ],
            )
            .mappings()
            .one()
        )

        connection.execute(
            sqlalchemy.text("""
                INSERT INTO wallet (user_id, from_bet, change)
                VALUES (:user_id, :bet_id, :change)
                """),
            [
                {
                    "user_id": user_id,
                    "bet_id": values["id"],
                    "change": new_bet.amount * -1,
                }
            ],
        )

        return BetResponse(
            bet_id=values["id"],
            game_id=new_bet.game_id,
            team_bet_on=new_bet.team,
            amount=new_bet.amount,
            odds=odds,
            potential_payout=odds * new_bet.amount,
            status="active",
            placed_at=str(values["created_at"]),
            new_balance=cur_balance - new_bet.amount,
        )
