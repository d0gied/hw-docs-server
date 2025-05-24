from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from analytics.config import Config


engine = create_async_engine(
    url=Config.Database.URL,
    echo=Config.Database.ECHO,
    pool_pre_ping=Config.Database.POOL_PRE_PING,
    pool_size=Config.Database.POOL_SIZE,
    max_overflow=Config.Database.MAX_OVERFLOW,
)
Session = async_sessionmaker(engine, expire_on_commit=False)
TABLE_ARGS = {"extend_existing": True, "schema": Config.Database.SCHEMA}


class Base(DeclarativeBase, AsyncAttrs):
    """
    Base class for all models.
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )


async def create_tables() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
