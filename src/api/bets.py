from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Annotated
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

class UserBet(BaseModel):
    bet_id: int
    game_id: int
    team_bet_on: str
    amount: float
    odds: float
    potential_payout: float
    status: str
    placed_at:str


class TotalUserBets(BaseModel):
    user_id: int
    status: str
    total:int
    bets:list[UserBet]



# @router.post("/create", status_code=status.HTTP_201_CREATED)
# def create_bet(user_id: int):
#     with db.engine.begin() as connection:
#         bet_id = connection.execute(
#             sqlalchemy.text("""
#                 INSERT INTO new_bets (user_id)
#                 VALUES (:user_id)
#                 RETURNING bet_id
#                 """),
#             [{"user_id": user_id}],
#         ).scalar_one()
#
#     return bet_id


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

@router.get("/users/{user_id}/bets")
def get_user_bets(user_id: int, status:str = "all"):

    if status not in ['all', 'won', 'lost']:
        raise HTTPException(
            status_code=400,
            detail = "Please enter a valid status"
        )

    
    if status == "won":

        with db.engine.begin() as connection:

            bets =connection.execute(
                sqlalchemy.text(
                    """
                    SELECT
                    bets.id, bets.game_id, teams.name, bets.amount,

                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds
                    
                    END AS odds,

                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds * bets.amount
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds * bets.amount
                    
                    END AS potential_payout,

                    bets.resolved,
                    bets.created_at
                    FROM bets

                    JOIN games ON bets.game_id = games.id
                    JOIN teams ON bets.team_id = teams.id

                    WHERE (bets.user_id = :user_id) AND (bets.team_id = games.winning_team_id) AND (games.winning_team_id IS NOT NULL) AND (bets.resolved = true)
                    """
                ),
                {"user_id": user_id},
            ).all()
            bets_list = []

            for bet in bets:
                bets_list.append(UserBet(bet_id=bet[0], game_id=bet[1], team_bet_on=bet[2], amount=bet[3], odds=bet[4], potential_payout=bet[5], status="won", placed_at=str(bet[7])))
    
        
        return TotalUserBets(user_id= user_id,
                             status= 'won',
                             total= len(bets_list),
                             bets= bets_list
                            )
    
    
    if status == 'lost':
        
        with db.engine.begin() as connection:
            bets = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT
                    bets.id, bets.game_id, teams.name, bets.amount,

                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds
                    
                    END AS odds,

                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds * bets.amount
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds * bets.amount
                    
                    END AS potential_payout,

                    bets.resolved,
                    bets.created_at
                    FROM bets

                    JOIN games ON bets.game_id = games.id
                    JOIN teams ON bets.team_id = teams.id

                    WHERE (bets.user_id = :user_id) AND (bets.team_id != games.winning_team_id) AND (games.winning_team_id IS NOT NULL) AND (bets.resolved = true)
                    """
                ),
                {"user_id": user_id}
            ).all()

            bets_list = []

            for bet in bets:
                bets_list.append(UserBet(bet_id=bet[0], game_id=bet[1], team_bet_on=bet[2], amount=bet[3], odds=bet[4], potential_payout=bet[5], status='lost', placed_at=str(bet[7])))
        
        return TotalUserBets(user_id= user_id,
                             status='lost',
                             total= len(bets_list),
                             bets= bets_list)
    

    else:

        with db.engine.begin() as connection:
            bets = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT
                    bets.id, bets.game_id, teams.name, bets.amount,

                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds
                    
                    END AS odds,

                    CASE
                        WHEN bets.team_id = games.home_team_id THEN games.home_odds * bets.amount
                        WHEN bets.team_id = games.away_team_id THEN games.away_odds * bets.amount
                    
                    END AS potential_payout,

                    bets.resolved,
                    bets.created_at,
                    games.winning_team_id,
                    bets.team_id
                    FROM bets

                    JOIN games ON bets.game_id = games.id
                    JOIN teams ON bets.team_id = teams.id

                    WHERE (bets.user_id = :user_id) AND (games.winning_team_id IS NOT NULL) AND (bets.resolved = true)
                    """
                ),
                {"user_id": user_id}
            ).all()

            bets_list = []

            for bet in bets:

                if bet[8] == bet[9]:
                    bets_list.append(UserBet(bet_id=bet[0], game_id=bet[1], team_bet_on=bet[2], amount=bet[3], odds=bet[4], potential_payout=bet[5], status='won', placed_at=str(bet[7])))
                
                elif bet[8] != bet[9]:
                     bets_list.append(UserBet(bet_id=bet[0], game_id=bet[1], team_bet_on=bet[2], amount=bet[3], odds=bet[4], potential_payout=bet[5], status='lost', placed_at=str(bet[7])))
        
        return TotalUserBets(user_id= user_id,
                             status='all',
                             total= len(bets_list),
                             bets= bets_list)


        



        




