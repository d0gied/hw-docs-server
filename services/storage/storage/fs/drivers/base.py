from abc import ABC, abstractmethod


class BaseFileStorageDriver(ABC):
    """
    Base class for file storage drivers.
    """

    @abstractmethod
    async def upload(self, file_path: str, data: bytes) -> None:
        """
        Upload a file to the storage.

        :param file_path: The path where the file will be stored.
        :param data: The data to be stored in the file.
        """

    @abstractmethod
    async def download(self, file_path: str) -> bytes:
        """
        Download a file from the storage.

        :param file_path: The path of the file to be downloaded.
        :return: The data of the downloaded file.
        """

    @abstractmethod
    async def delete(self, file_path: str) -> None:
        """
        Delete a file from the storage.

        :param file_path: The path of the file to be deleted.
        """
