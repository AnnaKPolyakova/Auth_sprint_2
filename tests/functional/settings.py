import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from tests.functional.logger import LOGGING

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env_test"), override=True)


class TestSettings(BaseSettings):
    REDIS_HOST: str = Field(env="REDIS_HOST", default='redis')
    REDIS_PORT: str = Field(env="REDIS_HOST", default='6379')
    REDIS_PROTOCOL: str = Field(env="REDIS_HOST", default='redis')

    POSTGRES_HOST: str = Field(env="REDIS_HOST", default='db')
    POSTGRES_PORT: int = Field(env="REDIS_HOST", default=5432)
    POSTGRES_DB: str = Field(env="REDIS_HOST", default='auth')
    POSTGRES_DB_TEST: str = Field(env="REDIS_HOST", default='auth_test')
    POSTGRES_USER: str = Field(env="REDIS_HOST", default='app')
    POSTGRES_PASSWORD: str = Field(env="REDIS_HOST", default='123qwe')
    JWT_SECRET_KEY: str = Field(
        env="REDIS_HOST",
        default='Y0QMIGwksa5OhtOBF9BczuAJ0hYMUv7esEBgMMdAuJ4V7stwxT9e'
    )
    DEFAULT_LIMITS: int = Field(env="REDIS_HOST", default=100)

    class Config:
        env_file = os.path.join(BASE_DIR, ".env", ".env_test")
        env_file_encoding = "utf-8"


logging_config.dictConfig(LOGGING)

test_settings = TestSettings()
