import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve()

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PROTOCOL: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_HOST: str
    # POSTGRES_PORT: int
    # POSTGRES_DB: str
    # POSTGRES_USER: str
    JWT_SECRET_KEY: str
    MAX_REQUEST_COUNT: int
    EX_TIME: int
    TIMOUT_FOR_REQUEST: int
    AUTH_HOST: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


auth_proxy_settings = Settings()
