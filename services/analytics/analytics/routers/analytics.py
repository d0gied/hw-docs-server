from typing import Annotated

from fastapi import APIRouter, Depends, Response, UploadFile
from fastapi.responses import FileResponse

from analytics.dependencies import AnalyticsServiceDep
from analytics.models.analytics import Analytics


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.post("/{file_id}")
async def analyze_file(
    file_id: int, analytics_service: AnalyticsServiceDep
) -> Analytics:
    """
    Analyze a file by its ID and return analytics results.

    :param file_id: The ID of the file to analyze.
    :param analytics_service: The AnalyticsService instance.
    :return: An Analytics object containing the results.
    """
    return await analytics_service.analyze_file(file_id)


@router.get("/{file_path:path}", response_class=FileResponse)
async def download_wordcloud(
    file_path: str, analytics_service: AnalyticsServiceDep
) -> Response:
    """
    Download the word cloud image for a specific file.

    :param path: The path to the word cloud image.
    :param analytics_service: The AnalyticsService instance.
    :return: A Response object containing the word cloud image.
    """
    return await analytics_service.download_wordcloud(file_path)
