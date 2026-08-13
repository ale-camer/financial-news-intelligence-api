import asyncio
from unittest.mock import MagicMock, patch

import pytest

from src.ingestion.orchestrator import run_ingestion
from src.schemas.article import RawArticle


@pytest.mark.asyncio
@patch("src.ingestion.orchestrator.fetch_newsapi_feed")
@patch("src.ingestion.orchestrator.fetch_rss_feed")
async def test_run_ingestion_success(mock_fetch_rss: MagicMock, mock_fetch_newsapi: MagicMock) -> None:
    # Arrange
    mock_fetch_rss.return_value = [{
        "title": "RSS Title",
        "link": "https://rss.example.com",
        "published_date": "2026-08-13",
        "author": "RSS Author",
        "summary": "RSS Summary",
        "source": "rss",
    }]
    
    mock_fetch_newsapi.return_value = [{
        "title": "NewsAPI Title",
        "link": "https://news.example.com",
        "published_date": "2026-08-13",
        "author": "NewsAPI Author",
        "summary": "NewsAPI Summary",
        "source": "newsapi",
    }]
    
    rss_urls = ["https://fake.rss"]
    newsapi_key = "fake_key"
    newsapi_query = "finance"
    
    # Act
    articles = await run_ingestion(newsapi_key, newsapi_query, rss_urls)
    
    # Assert
    assert len(articles) == 2
    assert all(isinstance(article, RawArticle) for article in articles)
    titles = [a.title for a in articles]
    assert "RSS Title" in titles
    assert "NewsAPI Title" in titles


@pytest.mark.asyncio
@patch("src.ingestion.orchestrator.fetch_newsapi_feed")
@patch("src.ingestion.orchestrator.fetch_rss_feed")
async def test_run_ingestion_partial_failures(mock_fetch_rss: MagicMock, mock_fetch_newsapi: MagicMock) -> None:
    # Arrange
    # One valid item, one corrupted item missing 'title'
    mock_fetch_rss.return_value = [
        {
            "title": "Valid RSS",
            "link": "https://rss.example.com",
            "published_date": "2026-08-13",
            "author": "RSS Author",
            "summary": "RSS Summary",
            "source": "rss",
        },
        {
            "link": "https://corrupted.example.com",
            "published_date": "2026-08-13",
            "author": "Bad Author",
            "summary": "Missing title",
            "source": "rss",
        }
    ]
    
    # NewsAPI client completely throws an exception
    mock_fetch_newsapi.side_effect = Exception("Critical Network Failure")
    
    # Act
    articles = await run_ingestion("key", "query", ["https://fake.rss"])
    
    # Assert
    # Should only return the single valid RSS article. The corrupt one is skipped, and NewsAPI exception is handled.
    assert len(articles) == 1
    assert articles[0].title == "Valid RSS"
