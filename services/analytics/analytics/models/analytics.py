from pydantic import BaseModel, Field


class Analytics(BaseModel):
    word_count: int = Field(..., description="Total number of words in the file")
    words_rates: dict[str, float] = Field(
        ..., description="Frequency of each word in the file"
    )
    unique_words: int = Field(
        ..., description="Total number of unique words in the file"
    )

    wordcloud_path: str | None = Field(
        None, description="Path to the generated word cloud image, if applicable"
    )
