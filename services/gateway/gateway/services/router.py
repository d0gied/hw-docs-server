from fastapi import Response, UploadFile, status
from fastapi.responses import Response
from httpx import AsyncClient


class RouterService:
    """
    A class to handle file storage operations.
    This class provides methods to upload, download, and delete files.
    """

    def __init__(self, storage_base_url: str, analytics_base_url: str) -> None:
        self.storage_client = AsyncClient(base_url=storage_base_url)
        self.analytics_client = AsyncClient(base_url=analytics_base_url)

    async def upload_file(self, file: UploadFile) -> Response:
        """
        Upload a file to the storage service.

        :param file: The file to be uploaded.
        :return: A response indicating the result of the upload operation.
        """
        async with self.storage_client as client:
            response = await client.post(
                "/files", files={"file": (file.filename, file.file, file.content_type)}
            )
            return Response(status_code=response.status_code, content=response.text)

    async def download_file_by_file_id(self, file_id: int) -> Response:
        """
        Download a file by its ID.

        :param file_id: The ID of the file to retrieve.
        :return: A response containing the file data.
        """
        async with self.storage_client as client:
            response = await client.get(f"/files/{file_id}")
            return Response(content=response.content, headers=response.headers)
