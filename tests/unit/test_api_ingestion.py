from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from src.api.main import create_app
from src.schemas.article import RawArticle
from src.storage.db import get_session


def test_trigger_ingestion() -> None:
    app = create_app()

    mock_raw_articles = [
        RawArticle(
            title="Raw Title",
            link="https://example.com/2",
            published_date="2026-08-14",
            author="Author",
            summary="Raw summary",
            source="newsapi",
        )
    ]

    mock_processed_dicts = [
        {
            "title": "Raw Title",
            "link": "https://example.com/2",
            "published_date": "2026-08-14",
            "author": "Author",
            "summary": "Raw summary",
            "source": "newsapi",
            "sentiment_score": 0.5,
            "sentiment_label": "neutral",
            "entities": [],
        }
    ]

    with patch("src.api.routes.ingestion.run_ingestion", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_raw_articles

        with patch(
            "src.api.routes.ingestion.process_batch", new_callable=AsyncMock
        ) as mock_process:
            mock_process.return_value = mock_processed_dicts

            mock_session = MagicMock()
            app.dependency_overrides[get_session] = lambda: mock_session

            client = TestClient(app)
            response = client.post("/api/v1/ingest/trigger")

            assert response.status_code == 200
            assert response.json() == {
                "status": "success",
                "articles_processed": 1,
                "articles_saved": 1,
            }
            mock_session.add.assert_called_once()
            mock_session.commit.assert_called_once()


def test_trigger_ingestion_empty_results() -> None:
    app = create_app()

    with patch("src.api.routes.ingestion.run_ingestion", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = []

        mock_session = MagicMock()
        app.dependency_overrides[get_session] = lambda: mock_session

        client = TestClient(app)
        response = client.post("/api/v1/ingest/trigger")

        assert response.status_code == 200
        assert response.json() == {
            "status": "success",
            "articles_processed": 0,
            "articles_saved": 0,
        }
