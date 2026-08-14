from fastapi.testclient import TestClient

from src.api.config import Settings
from src.api.main import create_app


def test_health_endpoint() -> None:
    app = create_app()
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "Financial News Intelligence API",
    }


def test_settings_default() -> None:
    s = Settings()
    assert s.PROJECT_NAME == "Financial News Intelligence API"
    assert s.API_V1_STR == "/api/v1"
