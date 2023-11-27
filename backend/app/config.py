import os
import boto3
from functools import lru_cache
from dotenv import load_dotenv

load_dotenv()


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

    # AWS Settings
    BUCKET_NAME = os.environ.get("BUCKET_NAME")
    s3 = boto3.client(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        config=boto3.session.Config(signature_version="s3v4"),
    )

    # AI Settings
    MODEL_PATH = os.environ.get("MODEL_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
