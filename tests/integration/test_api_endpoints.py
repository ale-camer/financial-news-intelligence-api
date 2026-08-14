from unittest.mock import AsyncMock, patch

import pytest
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.schemas.article import RawArticle
from src.storage.models import Article


@pytest.mark.asyncio
async def test_health_check_integration(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "app": "Financial News Intelligence API",
    }
    assert "X-Process-Time" in response.headers


@pytest.mark.asyncio
async def test_articles_list_and_filter_integration(
    async_client: AsyncClient, db_session: Session
) -> None:
    article1 = Article(
        title="Fed Raises Rates",
        link="https://example.com/fed-rates",
        published_date="2026-08-14",
        author="Reporter A",
        summary="Federal Reserve announced rate hike.",
        source="rss",
        sentiment_score=-0.8,
        sentiment_label="negative",
        entities=[{"text": "Fed", "label": "ORG"}],
    )
    article2 = Article(
        title="Tech Rally Continues",
        link="https://example.com/tech-rally",
        published_date="2026-08-14",
        author="Reporter B",
        summary="Tech stocks hit all-time high.",
        source="newsapi",
        sentiment_score=0.9,
        sentiment_label="positive",
        entities=[{"text": "Apple", "label": "ORG"}],
    )
    db_session.add_all([article1, article2])
    db_session.commit()

    # 1. Fetch all
    response = await async_client.get("/api/v1/articles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

    # 2. Filter by sentiment_label
    response = await async_client.get("/api/v1/articles", params={"sentiment_label": "positive"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Tech Rally Continues"
    assert data[0]["sentiment_label"] == "positive"


@pytest.mark.asyncio
async def test_article_sentiment_detail_integration(
    async_client: AsyncClient, db_session: Session
) -> None:
    article = Article(
        title="Market Analysis",
        link="https://example.com/market-analysis",
        published_date="2026-08-14",
        author="Analyst",
        summary="Detailed market analysis summary.",
        source="rss",
        sentiment_score=0.1,
        sentiment_label="neutral",
        entities=[{"text": "NASDAQ", "label": "ORG"}],
    )
    db_session.add(article)
    db_session.commit()
    db_session.refresh(article)

    # 1. Success fetch
    response = await async_client.get(f"/api/v1/articles/{article.id}/sentiment")
    assert response.status_code == 200
    assert response.json() == {
        "id": article.id,
        "sentiment_score": 0.1,
        "sentiment_label": "neutral",
        "entities": [{"text": "NASDAQ", "label": "ORG"}],
    }

    # 2. Not found
    response = await async_client.get("/api/v1/articles/999999/sentiment")
    assert response.status_code == 404
    assert response.json() == {"detail": "Article not found"}


@pytest.mark.asyncio
async def test_ingest_trigger_integration(async_client: AsyncClient) -> None:
    mock_raw = [
        RawArticle(
            title="Ingested Article",
            link="https://example.com/ingested-1",
            published_date="2026-08-14",
            author="Reporter",
            summary="Ingested summary",
            source="rss",
        )
    ]
    mock_processed = [
        {
            "title": "Ingested Article",
            "link": "https://example.com/ingested-1",
            "published_date": "2026-08-14",
            "author": "Reporter",
            "summary": "Ingested summary",
            "source": "rss",
            "sentiment_score": 0.75,
            "sentiment_label": "positive",
            "entities": [{"text": "Company", "label": "ORG"}],
        }
    ]

    with patch("src.api.routes.ingestion.run_ingestion", new_callable=AsyncMock) as mock_run:
        mock_run.return_value = mock_raw

        with patch(
            "src.api.routes.ingestion.process_batch", new_callable=AsyncMock
        ) as mock_process:
            mock_process.return_value = mock_processed

            response = await async_client.post("/api/v1/ingest/trigger")
            assert response.status_code == 200
            assert response.json() == {
                "status": "success",
                "articles_processed": 1,
                "articles_saved": 1,
            }

            # Verify persisted in DB via GET
            get_resp = await async_client.get("/api/v1/articles", params={"source": "rss"})
            assert get_resp.status_code == 200
            titles = [a["title"] for a in get_resp.json()]
            assert "Ingested Article" in titles
