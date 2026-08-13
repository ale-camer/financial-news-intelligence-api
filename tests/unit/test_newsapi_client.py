from unittest.mock import MagicMock, patch

import requests

from src.ingestion.newsapi_client import fetch_newsapi_feed

DUMMY_JSON_RESPONSE = {
    "status": "ok",
    "totalResults": 2,
    "articles": [
        {
            "source": {"id": "reuters", "name": "Reuters"},
            "author": "John Doe",
            "title": "Stock Market Hits Record High",
            "description": "The stock market went up today.",
            "url": "https://example.com/finance1",
            "urlToImage": "https://example.com/image1.jpg",
            "publishedAt": "2026-08-13T10:00:00Z",
            "content": "Full content here...",
        },
        {
            "source": {"id": None, "name": "Removed News"},
            "author": None,
            "title": "[Removed]",
            "description": "[Removed]",
            "url": "https://removed.com",
            "urlToImage": None,
            "publishedAt": "1970-01-01T00:00:00Z",
            "content": "[Removed]",
        },
    ],
}


@patch("src.ingestion.newsapi_client.requests.get")
def test_fetch_newsapi_feed_success(mock_get: MagicMock) -> None:
    # Setup mock response
    mock_response = MagicMock()
    mock_response.json.return_value = DUMMY_JSON_RESPONSE
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    query = "finance"
    api_key = "test_key"
    result = fetch_newsapi_feed(query, api_key)

    # Assert
    mock_get.assert_called_once_with(
        "https://newsapi.org/v2/everything",
        params={
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "apiKey": api_key,
        },
        timeout=10,
    )

    # We have 2 articles in the mock, but one is [Removed], so only 1 should be parsed
    assert len(result) == 1

    item = result[0]
    assert item["title"] == "Stock Market Hits Record High"
    assert item["link"] == "https://example.com/finance1"
    assert item["published_date"] == "2026-08-13T10:00:00Z"
    assert item["summary"] == "The stock market went up today."
    assert item["author"] == "John Doe"


@patch("src.ingestion.newsapi_client.requests.get")
def test_fetch_newsapi_feed_network_error(mock_get: MagicMock) -> None:
    # Setup mock to raise a RequestException (like a 401 Unauthorized or network timeout)
    mock_get.side_effect = requests.exceptions.RequestException("401 Unauthorized")

    # Act
    result = fetch_newsapi_feed("finance", "invalid_key")

    # Assert
    assert mock_get.called
    assert result == []


@patch("src.ingestion.newsapi_client.requests.get")
def test_fetch_newsapi_feed_invalid_json(mock_get: MagicMock) -> None:
    # Setup mock response that raises ValueError on .json() call
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("Invalid JSON format")
    mock_get.return_value = mock_response

    # Act
    result = fetch_newsapi_feed("finance", "test_key")

    # Assert
    assert mock_get.called
    assert result == []
