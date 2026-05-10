from typing import Annotated
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import APIRouter, Depends, status
from fastapi import APIRouter, Depends, status
from pydantic import BaseModel
import sqlalchemy
from src.api.user_helper import *
from src import database as db

router = APIRouter(prefix="/users", tags=["User"])


class Active_bets(BaseModel):
    team: str
    wagered: float
    potential: float


class Balance(BaseModel):
    balance: float


# How will potential payout be calculated


@router.get("/active_bets", response_model=list[Active_bets])
def get_active_bets(user_id: int) -> list[Active_bets]:

    with db.engine.begin() as connection:
        information = connection.execute(
            sqlalchemy.text("""
            SELECT teams.name, bets.amount,
                            CASE  WHEN bets.team_id = games.home_team_id THEN games.home_odds
                            ELSE
                                games.away_odds
                            END AS odds

            FROM bets
            JOIN teams ON bets.team_id = teams.id
            JOIN games ON games.id = bets.game_id
            WHERE bets.user_id = :id AND bets.resolved = FALSE
            """),
            {"id": user_id},
        ).all()

    bets = []
    for info in information:
        bets.append(Active_bets(team=info.name, wagered=info.amount, potential= round(info.amount +info.amount * info.odds,2)))

    return bets


@router.get("/Get_Balance", response_model=Balance)
def get_balance(user_id: int):

    with db.engine.begin() as connection:
        money = connection.execute(
            sqlalchemy.text("""
            SELECT COALESCE(SUM(change),0) AS balance
            FROM wallet
            WHERE wallet.user_id = :id

            """),
            {"id": user_id},
        )
    money = money.scalar_one()
    if money == None:
        raise HTTPException(status_code=404, detail="Could not find Wallet")

    return Balance(balance=money)


@router.get("/users/me/")
async def read_users_me(
    current_token_data: Annotated[TokenData, Depends(get_token_data)],
) -> TokenData:
    return current_token_data
