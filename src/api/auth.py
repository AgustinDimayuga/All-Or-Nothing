from datetime import datetime, timedelta, timezone
from os import access, name
from typing import Annotated


from sqlalchemy.exc import IntegrityError
import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from jwt import algorithms
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from pydantic import BaseModel


from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
import sqlalchemy
from sqlalchemy.engine import create
from src.api import auth
from src import database as db

from src.config import get_settings

settings = get_settings()
secret_key = settings.SECRET_KEY
algorithm = settings.ALGORITHM
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class TokenData(BaseModel):
    userId: int


class Token(BaseModel):
    access_token: str
    token_type: str


class UserCredInDB(BaseModel):
    user_id: int
    username: str
    hashed_password: str
    name: str


class User(BaseModel):
    name: str
    email: str
    username: str
    name: str


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
    JOIN user_creds ON user_id = id
    WHERE username = :username

    """),
            {"username": username},
        )
        .mappings()
        .one()
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


async def get_current_user(
    connection: sqlalchemy.Connection, token: Annotated[str, Depends(oauth2_scheme)]
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(userId=user_id)
    except InvalidTokenError:
        raise credentials_exception

    user = get_user_creds(connection, user_id)
    if user is None:
        raise credentials_exception
    return user


class PostUser(BaseModel):
    name: str
    email: str
    username: str
    password: str


@router.post("/users", response_model=Token)
def create_user(user: PostUser):

    try:
        with db.engine.begin() as connection:
            # Create new user in users table
            hashed_password = get_password_hash(user.password)
            user_id = connection.execute(
                sqlalchemy.text("""
                INSERT INTO users (name, email, username)
                VALUES (:name, :email, :username)
                RETURNING id
                """),
                {"name": user.name, "email": user.email, "username": user.username},
            ).scalar_one()

            # Store password in user_creds
            connection.execute(
                sqlalchemy.text("""
                INSERT INTO user_creds (user_id, password)
                VALUES (:user_id, :password)
                """),
                {"user_id": user_id, "password": hashed_password},
            )
            # TODO: Create Wallet

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )
    signed_token = create_access_token({"sub": user_id, "name": user.name})
    return Token(access_token=signed_token, token_type="bearer")


class SignIn(BaseModel):
    username: str
    password: str


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

    signed_token = create_access_token({"sub": user.user_id, "name": user.name})
    return Token(access_token=signed_token, token_type="bearer")
