import logging
import sys

import uvicorn
from fastapi import FastAPI
from loguru import logger

try:
    from app.loguru_handler import InterceptHandler
except ModuleNotFoundError:  # pragma: no cover - used when running the file directly
    from loguru_handler import InterceptHandler


# This setup runs once when the application starts. It is cleaner than config at
# import time because the logging system is initialized only when the app is
# actually running.
def configure_logging() -> None:
    # Remove the default Loguru sink so we can define our own format and level.
    logger.remove()
    
    # Console output
    logger.add(
        sys.stdout,
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {message}",
    )
    
    # File output
    logger.add(
        "file.log",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level:<8} | {message}",
    )

    # Route Python's logging records into Loguru. This catches logs from FastAPI,
    # Uvicorn, and any standard library logging calls.
    logging.basicConfig(
        handlers=[InterceptHandler()],
        level=logging.DEBUG,
        force=True,
    )

    # Apply the same handler to Uvicorn's loggers so request and server logs use
    # the same formatting and level thresholds.
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]


app: FastAPI = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
    version="0.1.0",
)


@app.on_event("startup")
async def startup_event() -> None:
    configure_logging()
    logger.info("Application startup complete")


@app.get("/")
async def read_root() -> dict[str, str]:
    logger.info("Root endpoint called")
    return {"Hello": "World"}


@app.get("/health")
async def health_check() -> dict[str, str]:
    logger.info("Health check endpoint called")
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
