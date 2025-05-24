from .drivers.base import BaseFileStorageDriver


class FilesStorage:
    def __init__(self, driver: BaseFileStorageDriver) -> None:
        """
        Initialize the FilesStorage with a specific driver.

        :param driver: The storage driver to be used.
        """
        self.driver = driver

    async def upload(self, file_path: str, data: bytes) -> None:
        """
        Upload a file to the storage.

        :param file_path: The path where the file will be stored.
        :param data: The data to be stored in the file.
        """
        await self.driver.upload(file_path, data)

    async def download(self, file_path: str) -> bytes:
        """
        Download a file from the storage.

        :param file_path: The path of the file to be downloaded.
        :return: The data of the downloaded file.
        """
        return await self.driver.download(file_path)
