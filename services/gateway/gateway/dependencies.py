from typing import Annotated

from fastapi import Depends, File
from httpx import AsyncClient

from gateway.config import Config
from gateway.services.router import RouterService


def get_router_service(config: Config = Depends(Config)) -> RouterService:
    """
    Dependency to get the RouterService instance.

    :param config: The configuration object.
    :return: An instance of RouterService.
    """
    return RouterService(
        storage_client=AsyncClient(base_url=config.STORAGE_SERVICE_URL),
        analytics_client=AsyncClient(base_url=config.ANALYTICS_SERVICE_URL),
    )


RouterServiceDep = Annotated[RouterService, Depends(get_router_service)]
