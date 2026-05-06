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

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class Token(BaseModel):
    access_token: str
    token_type: str


class PostUser(BaseModel):
    username: str
    name: str
    email: str
    phone: str
    password: str


@router.post("/users", response_model=Token)
def create_user(user: PostUser):

    try:
        with db.engine.begin() as connection:
            # Create new user in users table
            hashed_password = get_password_hash(user.password)
            user_id = connection.execute(
                sqlalchemy.text("""
                INSERT INTO users (username, name, email, phone)
                VALUES (:username, :name, :email, :phone)
                RETURNING id
                """),
                {
                    "username": user.username,
                    "name": user.name,
                    "email": user.email,
                    "phone": user.phone,
                },
            ).scalar_one()
            # Store password in user_creds
            connection.execute(
                sqlalchemy.text("""
                INSERT INTO user_cred (user_id, password)
                VALUES (:user_id, :password)
                """),
                {"user_id": user_id, "password": hashed_password},
            )
            # Give user 100 dollars as a Bonus
            connection.execute(
                sqlalchemy.text("""
                    INSERT INTO wallet (user_id,change)
                    VALUES(:user_id,:change)
                """),
                {"user_id": user_id, "change": 100},
            )

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    signed_token = create_access_token({"user_id": user_id, "name": user.name})
    return Token(access_token=signed_token, token_type="bearer")


@router.post("/tokens")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    with db.engine.begin() as connection:
        user = authenticate_user(connection, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    signed_token = create_access_token({"user_id": user.user_id, "name": user.name})
    return Token(access_token=signed_token, token_type="bearer")
