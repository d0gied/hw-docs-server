from dataclasses import dataclass

from httpx import AsyncClient


@dataclass
class FileData:
    file_name: str
    file_size: int
    file_type: str
    file_content: bytes


class StorageConnector:
    def __init__(self, storage_client: AsyncClient):
        self.client = storage_client

    async def download_file(self, file_id: int) -> FileData:
        """
        Download a file from the storage service by its ID.

        :param file_id: The ID of the file to download.
        :return: An instance of FileData containing file details.
        """
        async with self.client as client:
            response = await client.get(f"/files/{file_id}")
            response.raise_for_status()

            file_name = (
                response.headers.get("Content-Disposition")
                .split("filename=")[-1]
                .strip('"')
            )
            file_size = int(response.headers.get("Content-Length", 0))
            file_type = response.headers.get("Content-Type", "application/octet-stream")

            return FileData(
                file_name=file_name,
                file_size=file_size,
                file_type=file_type,
                file_content=response.content,
            )
