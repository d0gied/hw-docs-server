from os import getenv
from typing import Literal

from loguru import logger


class Config:
    STORAGE_SERVICE_URL: str = getenv("STORAGE_SERVICE_URL", "http://localhost:8001")
    ANALYTICS_SERVICE_URL: str = getenv(
        "ANALYTICS_SERVICE_URL", "http://localhost:8002"
    )
