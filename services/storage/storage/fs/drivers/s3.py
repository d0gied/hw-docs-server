from loguru import logger

from .base import BaseFileStorageDriver


logger.debug("Loading S3 storage driver module")


class S3StorageDriver(BaseFileStorageDriver):
    def __init__(
        self,
        endpoint_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str,
    ) -> None:
        """
        Initialize the S3 storage driver.

        :param endpoint_url: The S3 endpoint URL.
        :param access_key: The access key for S3.
        :param secret_key: The secret key for S3.
        :param bucket_name: The name of the S3 bucket.
        :param region: The AWS region where the bucket is located.
        """
        self.endpoint_url = endpoint_url
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.region = region

    async def upload(self, file_path: str, data: bytes) -> None: ...

    async def download(self, file_path: str) -> bytes: ...

    async def delete(self, file_path: str) -> None: ...
