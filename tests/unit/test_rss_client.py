from unittest.mock import MagicMock, patch

import requests

from src.ingestion.rss_client import fetch_rss_feed

# A minimal dummy RSS XML for testing
DUMMY_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Test Finance News</title>
    <link>http://example.com</link>
    <description>Financial test news</description>
    <item>
      <title>Test Article 1</title>
      <link>http://example.com/1</link>
      <pubDate>Thu, 13 Aug 2026 10:00:00 +0000</pubDate>
      <description>This is a test article.</description>
    </item>
  </channel>
</rss>
"""


@patch("src.ingestion.rss_client.requests.get")
def test_fetch_rss_feed_success(mock_get: MagicMock) -> None:
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = DUMMY_RSS.encode("utf-8")
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    url = "http://fakeurl.com/rss"
    result = fetch_rss_feed(url)

    # Assert
    mock_get.assert_called_once_with(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        timeout=10,
    )
    assert len(result) == 1

    item = result[0]
    assert item["title"] == "Test Article 1"
    assert item["link"] == "http://example.com/1"
    assert item["published_date"] == "Thu, 13 Aug 2026 10:00:00 +0000"
    assert item["summary"] == "This is a test article."
    assert item["author"] == ""


@patch("src.ingestion.rss_client.requests.get")
def test_fetch_rss_feed_network_error(mock_get: MagicMock) -> None:
    # Setup mock to raise a RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Network Error")

    # Act
    result = fetch_rss_feed("http://fakeurl.com/rss")

    # Assert
    assert mock_get.called
    assert result == []


@patch("src.ingestion.rss_client.requests.get")
def test_fetch_rss_feed_malformed_xml(mock_get: MagicMock) -> None:
    # Setup mock response with malformed XML
    mock_response = MagicMock()
    mock_response.content = b"Not an XML file"
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    result = fetch_rss_feed("http://fakeurl.com/rss")

    # Assert
    assert mock_get.called
    # feedparser returns an empty list for completely invalid non-XML strings
    assert result == []
