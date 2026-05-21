from fastapi import Header
from pydantic import BaseModel
from typing import Annotated


class IdempotencyKey(BaseModel):
    Idempotency_Key: str


def get_idempotency_key(ikey: Annotated[IdempotencyKey, Header()]):
    return ikey.Idempotency_Key
