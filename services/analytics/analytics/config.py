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

    class WordCloudApi:
        API_URL: str = getenv("WORDCLOUD_API_URL", "https://wordcloud.example.com/api")
        WORDCLOUD_API_KEY: str = getenv("WORDCLOUD_API_KEY", "your_api_key_here")
        TIMEOUT: int = int(getenv("WORDCLOUD_TIMEOUT", "10"))

    class Storage:
        API_URL: str = getenv("STORAGE_API_URL", "http://localhost:8001")

    class Filesystem:
        BASE_PATH: str = getenv("FILESYSTEM_BASE_PATH", "./.cache/analytics")
