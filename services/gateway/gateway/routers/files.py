from typing import Annotated

from fastapi import APIRouter, Depends, Response, UploadFile
from fastapi.responses import FileResponse

from gateway.dependencies import RouterServiceDep


router = APIRouter(prefix="/files", tags=["files"])


@router.get(
    "/{file_id}",
    responses={
        200: {"description": "File retrieved successfully"},
        404: {"description": "File not found"},
    },
    response_class=FileResponse,
)
async def get_file(file_id: int, router_service: RouterServiceDep) -> Response:
    """
    Retrieve a file by its ID.

    :param file_id: The ID of the file to retrieve.
    """
    return await router_service.download_file_by_file_id(file_id)


@router.post(
    "",
    responses={
        200: {"description": "File retrieved successfully"},
        201: {"description": "File uploaded successfully"},
        400: {"description": "Invalid file format or size"},
    },
    response_model=int,
)
async def upload_file(file: UploadFile, router_service: RouterServiceDep) -> Response:
    """
    Upload a file to the storage service.

    :param file: The file to be uploaded.
    :param storage_service: The storage service dependency.
    """
    return await router_service.upload_file(file)
