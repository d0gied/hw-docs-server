from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from httpx import ConnectError, ConnectTimeout
from loguru import logger

from gateway.exception_handler import connection_error_handler
from gateway.routers.files import router as files_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan event handler.
    This can be used to initialize resources or perform setup tasks.
    """

    logger.info("Starting application lifespan setup.")
    yield


app = FastAPI(
    title="Storage Service",
    description="A service for managing file storage operations.",
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

# if some services are not available, handle connection errors gracefully
app.add_exception_handler(ConnectError, connection_error_handler)
app.add_exception_handler(ConnectTimeout, connection_error_handler)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
