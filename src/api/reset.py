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
    prefix="/reset", tags= ["reset-DB"]
)


@router.post("/hello")
def reset_db():
    with db.engine.begin() as connection:
        connection.execute()
