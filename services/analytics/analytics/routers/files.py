from typing import Annotated

from fastapi import APIRouter, Depends, Response, UploadFile
from fastapi.responses import FileResponse


router = APIRouter(prefix="/analytics", tags=["analytics"])
