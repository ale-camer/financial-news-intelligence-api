from typing import Any

from fastapi import FastAPI

from src.api.config import settings


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

    return app


app = create_app()
