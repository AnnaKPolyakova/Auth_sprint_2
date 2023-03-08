import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"), override=True)


class Settings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PROTOCOL: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    JWT_SECRET_KEY: str
    PAGE_SIZE: int

    CLIENT_ID_YANDEX: str
    SECRET_YANDEX: str
    AUTH_URL_YANDEX: str
    TOKEN_URL_YANDEX: str
    USER_INFO_URL_YANDEX: str

    CLIENT_ID_VK: str
    SECRET_VK: str
    AUTH_URL_VK: str
    TOKEN_URL_VK: str
    VERSION_VK: str

    class Config:
        env_file = os.path.join(BASE_DIR, ".env")
        env_file_encoding = "utf-8"


settings = Settings()
