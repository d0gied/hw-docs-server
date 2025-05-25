from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from analytics.databases.base import create_tables
from analytics.routers.analytics import router as files_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.
    This can be used to initialize resources or perform setup tasks.
    """

    logger.info("Starting application lifespan setup.")
    await create_tables()
    logger.info("Database tables created successfully.")
    yield


app = FastAPI(
    title="Analytics Service",
    description="A service for managing file analytics operations.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(files_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
