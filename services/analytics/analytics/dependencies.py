from typing import Annotated

from connectors.wordcloud import WordCloudConnector
from fastapi import Depends, File
from httpx import AsyncClient

from analytics.config import Config


ConfigDep = Annotated[Config, Depends(Config)]


def get_wordcloud_connector(
    config: ConfigDep = Depends(Config),
) -> 'WordCloudConnector':
    """
    Dependency to get the WordCloudConnector instance.

    :param config: The configuration object.
    :return: An instance of WordCloudConnector.
    """
    return WordCloudConnector(
        wordcloud_client=AsyncClient(
            base_url=config.WordCloudApi.API_URL,
            timeout=config.WordCloudApi.TIMEOUT,
            headers={
                "Authorization": f"Bearer {config.WordCloudApi.WORDCLOUD_API_KEY}"
            },
        )
    )
