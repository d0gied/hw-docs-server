from typing import Annotated

from fastapi import Depends, File

from storage.config import Config
from storage.fs.drivers import FilesystemStorageDriver, S3StorageDriver
from storage.fs.drivers.base import BaseFileStorageDriver
from storage.fs.storage import FilesStorage
from storage.services.storage import StorageService


def get_files_storage(config: Config = Depends(Config)) -> FilesStorage:
    """
    Dependency to get the FilesStorage instance.

    :return: An instance of FilesStorage.
    """
    driver: 'BaseFileStorageDriver'
    match config.FilesStorage.BACKEND.lower():
        case 'local':
            driver = FilesystemStorageDriver(base_path=config.Local.BASE_DIR)
        case 's3':
            driver = S3StorageDriver(
                endpoint_url=config.S3.ENDPOINT_URL,
                access_key=config.S3.ACCESS_KEY,
                secret_key=config.S3.SECRET_KEY,
                bucket_name=config.S3.BUCKET_NAME,
                region=config.S3.REGION,
            )
        case _:
            raise ValueError(
                f"Unsupported storage backend: {Config.FilesStorage.BACKEND}"
            )

    return FilesStorage(driver=driver)


def get_storage_service(
    file_storage: Annotated[FilesStorage, Depends(get_files_storage)],
) -> 'StorageService':
    """
    Dependency to get the StorageService instance.

    :param file_storage: The FilesStorage instance.
    :return: An instance of StorageService.
    """
    return StorageService(file_storage)


StorageServiceDep = Annotated[StorageService, Depends(get_storage_service)]
