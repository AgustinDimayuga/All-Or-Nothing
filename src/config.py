from dotenv import find_dotenv, load_dotenv
import os
from functools import lru_cache

load_dotenv(dotenv_path="default.env", override=False)
load_dotenv(dotenv_path=find_dotenv(".env"), override=True)


class Settings:
    API_KEY: str | None = os.getenv("API_KEY")
    POSTGRES_URI: str | None = os.getenv("POSTGRES_URI")

    def __init__(self):
        if not self.API_KEY:
            raise ValueError("API_KEY is missing.")
        if not self.POSTGRES_URI:
            raise ValueError("POSTGRES_URI is missing.")


@lru_cache()
def get_settings():
    return Settings()
