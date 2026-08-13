from unittest.mock import MagicMock, patch

import requests

from src.ingestion.web_scraper import scrape_article_text

DUMMY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Main Title</h1>
    <p>This is the first paragraph.</p>
    <div>
        <p>This is the <b>second</b> paragraph.</p>
    </div>
    <span>Not a paragraph</span>
    <p>  This is the third paragraph with spaces.  </p>
</body>
</html>
"""


@patch("src.ingestion.web_scraper.requests.get")
def test_scrape_article_text_success(mock_get: MagicMock) -> None:
    # Setup mock response
    mock_response = MagicMock()
    mock_response.content = DUMMY_HTML.encode("utf-8")
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Act
    url = "https://fake-news-site.com/article"
    result = scrape_article_text(url)

    # Assert
    mock_get.assert_called_once_with(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
        timeout=10,
    )

    # Check that it extracted text only from <p> tags, parsed internal tags (like <b>), and stripped extra spaces
    expected_text = "This is the first paragraph. This is the second paragraph. This is the third paragraph with spaces."
    assert result == expected_text


@patch("src.ingestion.web_scraper.requests.get")
def test_scrape_article_text_network_error(mock_get: MagicMock) -> None:
    # Setup mock to raise a RequestException
    mock_get.side_effect = requests.exceptions.RequestException("Timeout Error")

    # Act
    result = scrape_article_text("https://error.com")

    # Assert
    assert mock_get.called
    assert result == ""


@patch("src.ingestion.web_scraper.requests.get")
def test_scrape_article_text_unexpected_error(mock_get: MagicMock) -> None:
    # Setup mock to raise a generic Exception
    mock_get.side_effect = Exception("Unexpected runtime error")

    # Act
    result = scrape_article_text("https://unexpected.com")

    # Assert
    assert mock_get.called
    assert result == ""
