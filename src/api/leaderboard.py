from datetime import datetime
import sqlalchemy
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src import database as db


router = APIRouter(
    prefix="/leaderboard",
    tags=["leaderboard"],
)




@router.get("")
def get_leaderboard(period= 'weekly', limit = 25):

    if period not in ['daily', 'weekly']:
        raise HTTPException(
            status_code=400,
            detail= "Please enter a valid period"
        )   

    if period == 'weekly':
    
        with db.engine.begin() as connection:
            users = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT users.username, users.id, COALESCE(SUM(wallet.change),0) AS net_earnings
                    FROM users
                    JOIN wallet ON users.id = wallet.user_id
                    JOIN bets ON wallet.from_bet = bets.id
                    WHERE (wallet.from_bet IS NOT NULL) AND (bets.created_at >= NOW() - INTERVAL '7 days')
                    GROUP BY users.username, users.id
                    ORDER BY Net_Earnings DESC
                    LIMIT :limit
                    """
                ),
                {"limit": limit}
            ).all()

            leaders = []

            for i in range(len(users)):
                leaders.append({
                    "rank": i+1,
                    "user_id": users[i][1],
                    "username": users[i][0],
                    "net_earnings": float(users[i][2])
                })

        return {
            "period": period,
            "limit": limit,
            "leaderboard": leaders,
        }
    
    if period == 'daily':

        with db.engine.begin() as connection:
            users = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT users.username, users.id, COALESCE(SUM(wallet.change),0) AS net_earnings
                    FROM users
                    JOIN wallet ON users.id = wallet.user_id
                    JOIN bets ON wallet.from_bet = bets.id
                    WHERE (wallet.from_bet IS NOT NULL) AND (bets.created_at >= NOW() - INTERVAL '1 day')
                    GROUP BY users.username, users.id
                    ORDER BY Net_Earnings DESC
                    LIMIT :limit
                    """
                ),
                {"limit": limit}
            ).all()

            leaders = []

            for i in range(len(users)):
                leaders.append({
                    "rank": i+1,
                    "user_id": users[i][1],
                    "username": users[i][0],
                    "net_earnings": float(users[i][2])
                })


        return {
            "period": period,
            "limit": limit,
            "leaderboard": leaders,
        }






    


