import hashlib
from typing import TYPE_CHECKING
from urllib.parse import quote

from fastapi import Response, UploadFile, status
from fastapi.responses import Response
from sqlalchemy import select


class AnalyticsService:
    """
    Service for handling analytics-related operations.
    """
