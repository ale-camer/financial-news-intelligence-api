from typing import Any

from fastapi import FastAPI

from src.api.config import settings
from src.api.exceptions import global_exception_handler
from src.api.middleware import add_process_time_header
from src.api.routes import articles, ingestion


def create_app() -> FastAPI:
    """
    Application factory for creating and configuring a FastAPI instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )

    # Register middleware and exception handlers
    app.middleware("http")(add_process_time_header)
    app.add_exception_handler(Exception, global_exception_handler)

    @app.get("/health", tags=["health"])
    async def health_check() -> dict[str, Any]:
        return {
            "status": "ok",
            "app": settings.PROJECT_NAME,
        }

    app.include_router(
        articles.router,
        prefix=settings.API_V1_STR + "/articles",
        tags=["articles"],
    )

    app.include_router(
        ingestion.router,
        prefix=settings.API_V1_STR + "/ingest",
        tags=["ingestion"],
    )

    return app


app = create_app()
