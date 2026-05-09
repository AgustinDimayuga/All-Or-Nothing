import json

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Annotated

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


class NewBetResponse(BaseModel):
    bet_id: int


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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=NewBetResponse)
def create_bet(current_token_data: Annotated[TokenData, Depends(get_token_data)]):
    with db.engine.begin() as connection:
        user_id = current_token_data.user_id

        bet_id = connection.execute(
            sqlalchemy.text("""
                INSERT INTO new_bet_ids (user_id)
                VALUES (:user_id)
                RETURNING bet_id
                """),
            [{"user_id": user_id}],
        ).scalar_one()

    return NewBetResponse(bet_id=bet_id)


@router.post("/{bet_id}/place", response_model=BetResponse)
def place_bet(
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
    new_bet: Bet,
    bet_id: int,
):

    with db.engine.begin() as connection:

        existing_bet = connection.execute(
            sqlalchemy.text("""
                SELECT response
                FROM processed_bets
                WHERE bet_id = :bet_id
                """),
            [{"bet_id": bet_id}],
        ).scalar_one_or_none()

        if existing_bet:
            return existing_bet

            raise HTTPException(status_code=409, detail="Bet has already been placed")

        user_id = current_token_data.user_id

        if new_bet.amount <= 0:
            raise HTTPException(
                status_code=400, detail="bet amount cannot be 0 or negative"
            )

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
                SELECT home_team_id, away_team_id, home_odds, away_odds, teams.id AS team_id
                FROM games
                JOIN teams ON teams.id = games.home_team_id OR teams.id = games.away_team_id
                WHERE games.id = :game_id AND teams.name = :team_name
                """),
                [{"game_id": new_bet.game_id, "team_name": new_bet.team}],
            )
            .mappings()
            .one_or_none()
        )

        if not get_odds:
            raise HTTPException(
                status_code=400,
                detail="Team is not playing or team or game does not exist",
            )

        team_id = get_odds["team_id"]

        if team_id == get_odds["home_team_id"]:
            odds = get_odds["home_odds"]
        elif team_id == get_odds["away_team_id"]:
            odds = get_odds["away_odds"]

        values = (
            connection.execute(
                sqlalchemy.text("""
                INSERT INTO bets (id, user_id, game_id, team_id, amount)
                VALUES (:id, :user_id, :game_id, :team_id, :amount)
                RETURNING id, created_at
                """),
                [
                    {
                        "id": bet_id,
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

        bet_response = BetResponse(
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

        connection.execute(
            sqlalchemy.text("""
                INSERT INTO processed_bets (bet_id, response)
                VALUES (:bet_id, :response)
                """),
            [{"bet_id": bet_id, "response": json.dumps(bet_response.model_dump())}],
        )

        return bet_response
