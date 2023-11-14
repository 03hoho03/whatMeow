import os
from functools import lru_cache


class Settings:
    # DB Settings
    DB_USERNAME = os.environ.get("DB_USERNAME")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_NAME = os.environ.get("DB_NAME")
    DB_PORT = int(os.environ.get("DB_PORT"))

    # Auth Settings
    SECRET_ACCESS_KEY = os.environ.get("SECRET_ACCESS_KEY")
    SECRET_REFRESH_KEY = os.environ.get("SECRET_REFRESH_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")

    # Kakao Settings
    KAKAO_CLIENT_ID = os.environ.get("KAKAO_CLIENT_ID")
    KAKAO_CLIENT_SECRET = os.environ.get("KAKAO_CLIENT_SECRET")
    KAKAO_REDIRECT_URI = os.environ.get("KAKAO_REDIRECT_URI")

    # Google Settings
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
