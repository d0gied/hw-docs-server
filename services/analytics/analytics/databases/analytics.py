from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import TABLE_ARGS, Base


class AnalyticsResult(Base):
    """
    Model for storing file metadata.
    """

    __tablename__ = "analytics_results"
    __table_args__ = (TABLE_ARGS,)

    file_id: Mapped[int] = (
        mapped_column(  # TODO: Use ForeignKey to link to a file table
            nullable=False,
            index=True,
            doc="ID of the file associated with the analytics result",
        )
    )
    result: Mapped[dict] = mapped_column(
        JSONB, nullable=False, doc="The analytics result data in JSON format"
    )
    wordcloud_path: Mapped[str] = mapped_column(
        nullable=True, doc="Path to the generated image, if applicable"
    )
    status: Mapped[str] = mapped_column(
        nullable=False,
        doc="Status of the analytics result (e.g., 'pending', 'completed')",
    )
