from sqlalchemy.orm import Mapped, mapped_column

from .base import TABLE_ARGS, Base


class File(Base):
    """
    Model for storing file metadata.
    """

    __tablename__ = "files"
    __table_args__ = (TABLE_ARGS,)

    name: Mapped[str]
    hash: Mapped[str] = mapped_column(nullable=False, unique=True)
    size: Mapped[int]
    mime_type: Mapped[str]

    content_path: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )  # Path to the file content
