import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

from tests.functional.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env_test"), override=True)


class TestSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PROTOCOL: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_DB_TEST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    JWT_SECRET_KEY: str = "test"
    DEFAULT_LIMITS: int

    class Config:
        env_file = os.path.join(BASE_DIR, ".env", ".env_test")
        env_file_encoding = "utf-8"


logging_config.dictConfig(LOGGING)

test_settings = TestSettings()
