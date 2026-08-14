from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.api.main import create_app
from src.storage.db import get_session
from src.storage.models import Article


def test_get_articles_empty() -> None:
    app = create_app()

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []

    app.dependency_overrides[get_session] = lambda: mock_session

    client = TestClient(app)
    response = client.get("/api/v1/articles")

    assert response.status_code == 200
    assert response.json() == []


def test_get_articles_with_results_and_filtering() -> None:
    app = create_app()

    mock_article = Article(
        id=1,
        title="Test Title",
        link="https://example.com/1",
        published_date="2026-08-14",
        author="Reporter",
        summary="Summary test",
        source="rss",
        sentiment_score=0.9,
        sentiment_label="positive",
        entities=[{"text": "Apple", "label": "ORG"}],
    )

    mock_session = MagicMock()
    mock_query = MagicMock()
    mock_session.query.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [mock_article]

    app.dependency_overrides[get_session] = lambda: mock_session

    client = TestClient(app)
    response = client.get(
        "/api/v1/articles",
        params={"skip": 0, "limit": 5, "source": "rss", "sentiment_label": "positive"},
    )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["title"] == "Test Title"
    assert data[0]["sentiment_label"] == "positive"
