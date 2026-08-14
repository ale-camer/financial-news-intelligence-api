from typing import Any

from fastapi import FastAPI

from src.api.config import settings
from src.api.routes import articles


def create_app() -> FastAPI:
    """
    Application factory for creating and configuring a FastAPI instance.
    """
    app = FastAPI(
        title=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )

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

    return app


app = create_app()
