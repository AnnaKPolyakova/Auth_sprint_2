import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, "../.env"), override=True)


class Settings(BaseSettings):
    REDIS_HOST: str = Field(env="REDIS_HOST", default='redis')
    REDIS_PORT: int = Field(env="REDIS_PORT", default=6379)
    REDIS_PROTOCOL: str = Field(env="REDIS_PROTOCOL", default='redis')
    POSTGRES_PASSWORD: str = Field(env="POSTGRES_PASSWORD", default='123qwe')
    POSTGRES_HOST: str = Field(env="POSTGRES_HOST", default='localhost')
    POSTGRES_PORT: int = Field(env="POSTGRES_PORT", default=5432)
    POSTGRES_DB: str = Field(env="POSTGRES_DB", default='auth_test')
    POSTGRES_USER: str = Field(env="POSTGRES_USER", default='app')
    JWT_SECRET_KEY: str = Field(
        env="JWT_SECRET_KEY",
        default='Y0QMIGwksa5OhtOBF9BczuAJ0hYMUv7esEBgMMdAuJ4V7stwxT9e'
    )
    PAGE_SIZE: int = Field(env="PAGE_SIZE", default=5)

    CLIENT_ID_YANDEX: str = Field(
        env="CLIENT_ID_YANDEX",
        default='456d38cbe52046f7b0835b029418a870'
    )
    SECRET_YANDEX: str = Field(
        env="SECRET_YANDEX", default='58e3b251a37440dd8ffee7ce9d8abd26'
    )
    AUTH_URL_YANDEX: str = Field(
        env="AUTH_URL_YANDEX", default='https://oauth.yandex.ru/authorize'
    )
    TOKEN_URL_YANDEX: str = Field(
        env="TOKEN_URL_YANDEX", default='https://oauth.yandex.ru/token'
    )
    USER_INFO_URL_YANDEX: str = Field(
        env="USER_INFO_URL_YANDEX", default='https://login.yandex.ru/info'
    )

    CLIENT_ID_VK: str = Field(env="CLIENT_ID_VK", default='51575191')
    SECRET_VK: str = Field(env="SECRET_VK", default='ZhuGwb4vskRlRfWhjP9k')
    AUTH_URL_VK: str = Field(
        env="AUTH_URL_VK", default='https://oauth.vk.com/authorize'
    )
    TOKEN_URL_VK: str = Field(
        env="TOKEN_URL_VK", default='https://oauth.vk.com/access_token'
    )
    VERSION_VK: str = Field(env="VERSION_VK", default='5.131')

    AGENT_HOST_NAME: str = Field(env="AGENT_HOST_NAME", default='jaeger')
    AGENT_PORT: int = Field(env="AGENT_PORT", default=6831)
    DEFAULT_LIMITS: int = Field(env="DEFAULT_LIMITS", default=100)
    TRACER_ON: int = Field(env="TRACER_ON", default=100)

    class Config:
        env_file = os.path.join(BASE_DIR, "../.env")
        env_file_encoding = "utf-8"


settings = Settings()
