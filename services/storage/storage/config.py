from os import getenv
from typing import Literal

from loguru import logger


class Config:
    class Database:
        URL = getenv(
            "DATABASE_URL",
            "postgresql+asyncpg://postgres:password@localhost:5432/postgres",
        )
        SCHEMA = getenv("DATABASE_SCHEMA", "public")
        ECHO = getenv("DATABASE_ECHO", "false").lower() == "true"
        POOL_PRE_PING = getenv("DATABASE_POOL_PRE_PING", "true").lower() == "true"
        POOL_SIZE = int(getenv("DATABASE_POOL_SIZE", 5))
        MAX_OVERFLOW = int(getenv("DATABASE_MAX_OVERFLOW", 10))

    class FilesStorage:
        BACKEND: str = getenv("FILES_STORAGE_BACKEND", "LOCAL")
        FILES_DIR: str = getenv("FILES_STORAGE_FILES_DIR", "files")

    class S3:
        ENDPOINT_URL = getenv("S3_ENDPOINT_URL", "https://s3.amazonaws.com")
        ACCESS_KEY = getenv("S3_ACCESS_KEY", "your_access_key")
        SECRET_KEY = getenv("S3_SECRET_KEY", "your_secret_key")
        BUCKET_NAME = getenv("S3_BUCKET_NAME", "your_bucket_name")
        REGION = getenv("S3_REGION", "us-east-1")

    class Local:
        BASE_DIR = getenv("LOCAL_STORAGE_BASE_DIR", "./.cache")
