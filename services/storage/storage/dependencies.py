from typing import Annotated

from fastapi import Depends

from storage.config import Config
from storage.fs.drivers.base import BaseFileStorageDriver
from storage.fs.storage import FilesStorage
from storage.services.storage import StorageService


ConfigDep = Annotated[Config, Depends(Config)]


def get_files_storage_driver(config: ConfigDep) -> BaseFileStorageDriver:
    """
    Dependency to get the BaseFileStorageDriver instance.

    :param config: The configuration object.
    :return: An instance of BaseFileStorageDriver.
    """

    match config.FilesStorage.BACKEND.lower():
        case 'local':
            from storage.fs.drivers.filesystem import (
                FilesystemStorageDriver,  # lazy import
            )

            return FilesystemStorageDriver(base_path=config.Local.BASE_DIR)
        case 's3':
            from storage.fs.drivers.s3 import S3StorageDriver  # lazy import

            return S3StorageDriver(
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


def get_files_storage(
    driver: Annotated[BaseFileStorageDriver, Depends(get_files_storage_driver)],
) -> FilesStorage:
    """
    Dependency to get the FilesStorage instance.

    :return: An instance of FilesStorage.
    """

    return FilesStorage(driver=driver)


FilesStorageDep = Annotated[FilesStorage, Depends(get_files_storage)]


def get_storage_service(
    config: ConfigDep, file_storage: FilesStorageDep
) -> 'StorageService':
    """
    Dependency to get the StorageService instance.

    :param file_storage: The FilesStorage instance.
    :return: An instance of StorageService.
    """
    return StorageService(file_storage, files_dir=config.FilesStorage.FILES_DIR)


StorageServiceDep = Annotated[StorageService, Depends(get_storage_service)]
