import hashlib
from typing import TYPE_CHECKING
from urllib.parse import quote

from fastapi import Response, UploadFile, status
from fastapi.responses import Response
from sqlalchemy import select

from storage.databases.base import Session
from storage.databases.files import File as DBFile


if TYPE_CHECKING:
    from fs.storage import FilesStorage


def sha256(data: bytes) -> str:
    """
    Calculate the SHA-256 hash of the given data.
    :param data: The data to hash.
    :return: The SHA-256 hash as a hexadecimal string.
    """
    return hashlib.sha256(data).hexdigest()


class StorageService:
    """
    A class to handle file storage operations.
    This class provides methods to upload, download, and delete files.
    """

    file_storage: 'FilesStorage'

    def __init__(self, file_storage: 'FilesStorage', files_dir: str) -> None:
        self.file_storage = file_storage
        self.files_dir = files_dir

    async def upload_file(self, file: UploadFile) -> Response:
        data = await file.read()
        file_hash = sha256(data)
        content_path = f"{self.files_dir}/{file_hash}"

        async with Session.begin() as session:
            query = await session.execute(
                select(DBFile).where(DBFile.hash == file_hash)
            )
            existing_file = query.scalars().first()
            if existing_file:
                return Response(
                    content=str(existing_file.id),
                    status_code=status.HTTP_200_OK,
                    media_type="text/plain",
                )
            else:
                await self.file_storage.upload(content_path, data)

                db_file = DBFile(
                    name=file.filename,
                    hash=file_hash,
                    size=len(data),
                    mime_type=file.content_type,
                    content_path=content_path,
                )
                session.add(db_file)
                await session.commit()

                return Response(
                    content=str(db_file.id),
                    status_code=status.HTTP_201_CREATED,
                    media_type="text/plain",
                )

    async def download_file_by_file_id(self, file_id: int) -> Response:
        async with Session() as session:
            query = await session.execute(select(DBFile).where(DBFile.id == file_id))
            db_file = query.scalars().first()
            if db_file:
                content = await self.file_storage.download(db_file.content_path)
                return Response(
                    content=content,
                    media_type=db_file.mime_type,
                    headers={
                        "Content-Disposition": f"attachment; filename*=utf-8''{quote(db_file.name)}"
                    },
                )
            return Response(status_code=status.HTTP_404_NOT_FOUND)

    async def download_file_by_path(self, file_path: str) -> Response:
        file_path = file_path.lstrip("/")
        if not file_path:
            return Response(status_code=status.HTTP_400_BAD_REQUEST)

        async with Session() as session:
            query = await session.execute(
                select(DBFile).where(DBFile.content_path == file_path)
            )
            db_file = query.scalars().first()
            if db_file:
                content = await self.file_storage.download(db_file.content_path)
                return Response(
                    content=content,
                    media_type=db_file.mime_type,
                    headers={
                        "Content-Disposition": f"attachment; filename*=utf-8''{quote(db_file.name)}"
                    },
                )
            return Response(status_code=status.HTTP_404_NOT_FOUND)
