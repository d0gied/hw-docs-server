from httpx import AsyncClient


class WordCloudConnector:
    def __init__(self, wordcloud_client: AsyncClient):
        self.client = wordcloud_client

    async def generate_wordcloud(self, text: str) -> bytes:
        """
        Generate a word cloud from the text file identified by file_id.

        :param file_id: The ID of the text file to process.
        :return: The generated word cloud image as bytes.
        """
        async with self.client as client:
            response = await client.post("/wordcloud", json={"text": text})
            response.raise_for_status()
            return response.content
