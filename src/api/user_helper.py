from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel

from src.database import get_connection

from fastapi import Depends, HTTPException, status

import sqlalchemy

from src.config import get_settings


class TokenData(BaseModel):
    user_id: int
    name: str


class UserCredInDB(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    name: str


settings = get_settings()
secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/tokens")

DUMMY_HASH = password_hash.hash("dummypassword")


def verify_passwword(plain_pass, hashed_password):
    return password_hash.verify(plain_pass, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user_creds(connection: sqlalchemy.Connection, username: str) -> UserCredInDB:
    ## Implement getting user
    user = (
        connection.execute(
            sqlalchemy.text("""
    SELECT id, username, password, name
    FROM users
    JOIN user_cred ON user_id = id
    WHERE username = :username

    """),
            {"username": username},
        )
        .mappings()
        .one_or_none()
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return UserCredInDB(
        user_id=user["id"],
        username=user["username"],
        hashed_password=user["password"],
        name=user["name"],
    )


def authenticate_user(connection: sqlalchemy.Connection, username: str, password: str):
    user = get_user_creds(connection, username)
    ## Protect Against time attackks
    if not user:
        verify_passwword(password, DUMMY_HASH)
        return False
    if not verify_passwword(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=45)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


async def get_token_data(
    connection: Annotated[sqlalchemy.Connection, Depends(get_connection)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        print(payload)
        user_id = payload.get("user_id")
        name = payload.get("name")

        if user_id is None or name is None:
            raise credentials_exception

    except InvalidTokenError as e:
        print(e)
        raise credentials_exception

    return TokenData(user_id=user_id, name=name)
