from typing import TYPE_CHECKING

from fastapi import HTTPException, Response, UploadFile, status
from fastapi.background import P
from fastapi.responses import Response
from httpx import ConnectError
from loguru import logger
from sqlalchemy import select

from analytics.databases.analytics import AnalyticsResult
from analytics.databases.base import Session
from analytics.models import analytics as analytics_models


if TYPE_CHECKING:
    from analytics.connectors.storage import StorageConnector
    from analytics.connectors.wordcloud import WordCloudConnector
    from analytics.fs.filesystem import FilesystemStorageDriver


class AnalyticsService:
    """
    Service for handling analytics-related operations.
    """

    def __init__(
        self,
        wordcloud_connector: 'WordCloudConnector',
        filesystem_storage_driver: 'FilesystemStorageDriver',
        storage_connector: 'StorageConnector',
    ) -> None:
        """
        Initialize the AnalyticsService with a WordCloudConnector.

        :param wordcloud_connector: An instance of WordCloudConnector.
        """
        self.wordcloud_connector = wordcloud_connector
        self.filesystem_storage_driver = filesystem_storage_driver
        self.storage_connector = storage_connector

    async def _fetch_file_content(self, file_id: int) -> str | None:
        """
        Fetch the content of a file by its ID.

        :param file_id: The ID of the file to fetch.
        :return: The content of the file as a string, or None if not found.
        """
        file = await self.storage_connector.download_file(file_id)
        if file is None:
            return None

        if file.file_type.startswith("text/"):
            return file.file_content.decode("utf-8")

        return None

    def _calculate_analytics(self, file_content: str) -> dict:
        """
        Calculate analytics from the file content.

        :param file_content: The content of the file.
        :return: A dictionary containing analytics results.
        """
        # Example analytics calculation
        word_count = len(file_content.split())
        words_rates = {
            word: file_content.count(word) / word_count
            for word in set(file_content.split())
        }
        unique_words = len(words_rates)

        return {
            "word_count": word_count,
            "words_rates": words_rates,
            "unique_words": unique_words,
        }

    async def analyze_file(self, file_id: int) -> analytics_models.Analytics:
        """
        Analyze the uploaded file and return the result.

        :param file_id: The ID of the file to analyze.
        :return: An Analytics object containing the results.
        """
        async with Session() as session:
            query = select(AnalyticsResult).where(AnalyticsResult.file_id == file_id)
            result = await session.execute(query)
            analytics_result = result.scalar_one_or_none()

            analytics: dict | None = None
            wordcloud_path: str | None = None

            if analytics_result is None:
                # Fetch the file content from the storage connector
                file_content = await self._fetch_file_content(file_id)

                if not file_content:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="File not found or unsupported file type.",
                    )

                # Generate word cloud
                try:
                    wordcloud_image = await self.wordcloud_connector.generate_wordcloud(
                        file_content
                    )
                except ConnectError as e:
                    pass
                else:
                    # Save the word cloud image to the filesystem
                    wordcloud_path = f"{file_id}/wordcloud.png"
                    await self.filesystem_storage_driver.upload(
                        wordcloud_path, wordcloud_image
                    )

                # Calculate analytics
                analytics = self._calculate_analytics(file_content)

                session.begin()
                # Create a new analytics result entry
                analytics_result = AnalyticsResult(
                    file_id=file_id,
                    result=analytics,
                    wordcloud_path=wordcloud_path,
                    status="completed",
                )
                session.add(analytics_result)
                await session.commit()
            else:
                analytics = analytics_result.result
                wordcloud_path = analytics_result.wordcloud_path

            return analytics_models.Analytics(
                word_count=analytics.get("word_count", 0),
                words_rates=analytics.get("words_rates", {}),
                unique_words=analytics.get("unique_words", 0),
                wordcloud_path=wordcloud_path,
            )

    async def download_wordcloud(self, file_path: str) -> Response:
        """
        Download the word cloud image.

        :param file_path: The path to the word cloud image.
        :return: A FileResponse containing the word cloud image.
        """
        logger.info(f"Downloading word cloud image from {file_path}")
        async with Session() as session:
            query = select(AnalyticsResult).where(
                AnalyticsResult.wordcloud_path == file_path
            )
            result = await session.execute(query)
            analytics_result = result.scalar_one_or_none()
            if analytics_result is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Word cloud image not found.",
                )

            if not await self.filesystem_storage_driver.exists(file_path):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Word cloud image not found.",
                )

            return Response(
                content=await self.filesystem_storage_driver.download(file_path),
                media_type="image/png",
                headers={"Content-Disposition": "attachment; filename=wordcloud.png"},
            )
