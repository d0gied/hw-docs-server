from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from httpx import AsyncClient

from analytics.config import Config
from analytics.services.analytics import AnalyticsService


if TYPE_CHECKING:
    from analytics.connectors.storage import StorageConnector
    from analytics.connectors.wordcloud import WordCloudConnector
    from analytics.fs.filesystem import FilesystemStorageDriver

ConfigDep = Annotated[Config, Depends(Config)]


def get_wordcloud_connector(config: ConfigDep) -> 'WordCloudConnector':
    """
    Dependency to get the WordCloudConnector instance.

    :param config: The configuration object.
    :return: An instance of WordCloudConnector.
    """
    from analytics.connectors.wordcloud import WordCloudConnector

    return WordCloudConnector(
        wordcloud_client=AsyncClient(
            base_url=config.WordCloudApi.API_URL,
            timeout=config.WordCloudApi.TIMEOUT,
            headers={
                "Authorization": f"Bearer {config.WordCloudApi.WORDCLOUD_API_KEY}"
            },
        )
    )


WordCloudConnectorDep = Annotated[
    'WordCloudConnector', Depends(get_wordcloud_connector)
]


def get_filesystem_storage_driver(config: ConfigDep) -> 'FilesystemStorageDriver':
    """
    Dependency to get the FilesystemStorageDriver instance.

    :param config: The configuration object.
    :return: An instance of FilesystemStorageDriver.
    """
    from analytics.fs.filesystem import FilesystemStorageDriver

    return FilesystemStorageDriver(base_path=config.Filesystem.BASE_PATH)


FilesystemStorageDriverDep = Annotated[
    'FilesystemStorageDriver', Depends(get_filesystem_storage_driver)
]


def get_storage_connector(config: ConfigDep) -> 'StorageConnector':
    """
    Dependency to get the StorageConnector instance.

    :param config: The configuration object.
    :return: An instance of StorageConnector.
    """
    from analytics.connectors.storage import StorageConnector

    return StorageConnector(AsyncClient(base_url=config.Storage.API_URL))


StorageConnectorDep = Annotated['StorageConnector', Depends(get_storage_connector)]


def get_analytics_service(
    wordcloud_connector: WordCloudConnectorDep,
    filesystem_storage_driver: FilesystemStorageDriverDep,
    storage_connector: StorageConnectorDep,
) -> 'AnalyticsService':
    """
    Dependency to get the AnalyticsService instance.

    :param wordcloud_connector: The WordCloudConnector instance.
    :return: An instance of AnalyticsService.
    """
    from analytics.services.analytics import AnalyticsService

    return AnalyticsService(
        wordcloud_connector=wordcloud_connector,
        filesystem_storage_driver=filesystem_storage_driver,
        storage_connector=storage_connector,
    )


AnalyticsServiceDep = Annotated['AnalyticsService', Depends(get_analytics_service)]
