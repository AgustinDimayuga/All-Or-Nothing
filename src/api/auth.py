from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel


from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from src.api import auth
from src import database as db

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenData(BaseModel):
    userId: int


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCredInDB(BaseModel):
    user_id: int
    username: str
    hashed_password: str


class User(BaseModel):
    id: int
    name: str
    email: str
    phone: str


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="tokens")
app = FastAPI()


def verify_passwword(plain_pass, hashed_password):
    return password_hash.verify(plain_pass, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(username: str):
    return UserCredInDB(user_id=1, username="hello", hashed_password="some-hash")


def authenticate_user(username: str, password: str):
    user = get_user(username)

    if not user:
        verify_passwword(password, user.has)
