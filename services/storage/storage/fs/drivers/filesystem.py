from pathlib import Path
from typing import override

import aiofiles

from storage.config import Config

from .base import BaseFileStorageDriver


class FilesystemStorageDriver(BaseFileStorageDriver):
    def __init__(self, base_path: str = Config.Local.BASE_DIR) -> None:
        """
        Initialize the filesystem storage driver.

        :param base_path: The base path for the storage.
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    @override
    async def upload(self, file_path: str, data: bytes) -> None:
        full_path = self.base_path / file_path

        if full_path.exists():
            raise FileExistsError(f"File {file_path} already exists in storage.")

        if not full_path.is_relative_to(self.base_path):
            raise ValueError("File path must be within the base path.")

        full_path.parent.mkdir(parents=True, exist_ok=True)

        async with aiofiles.open(str(full_path), "wb") as f:
            await f.write(data)

    @override
    async def download(self, file_path: str) -> bytes:
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"File {file_path} not found in storage.")

        async with aiofiles.open(self.base_path / file_path, "rb") as f:
            return await f.read()

    @override
    async def delete(self, file_path: str) -> None: ...
