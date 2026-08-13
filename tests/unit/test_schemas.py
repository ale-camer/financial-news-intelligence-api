import pytest
from pydantic import ValidationError

from src.schemas.article import ProcessedArticle, RawArticle


def test_raw_article_valid_data() -> None:
    # Arrange
    data = {
        "title": "Stock Market Up",
        "link": "https://finance.example.com",
        "published_date": "2026-08-13T10:00:00Z",
        "author": "Jane Doe",
        "summary": "The market saw a significant increase today.",
        "source": "newsapi",
    }

    # Act
    article = RawArticle.model_validate(data)

    # Assert
    assert article.title == "Stock Market Up"
    assert article.link == "https://finance.example.com"
    assert article.source == "newsapi"


def test_raw_article_missing_fields() -> None:
    # Arrange: Missing required fields like 'title' and 'link'
    data = {
        "published_date": "2026-08-13T10:00:00Z",
        "author": "Jane Doe",
        "summary": "Missing title",
        "source": "rss",
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        RawArticle.model_validate(data)

    # Verify that the validation error correctly complains about the missing fields
    assert "title\n  Field required" in str(exc_info.value)
    assert "link\n  Field required" in str(exc_info.value)


def test_processed_article_valid_data() -> None:
    # Arrange
    data = {
        "title": "Tech Stocks Rally",
        "link": "https://tech.example.com",
        "published_date": "2026-08-13",
        "author": "Tech Reporter",
        "summary": "Tech stocks are rallying again.",
        "source": "rss",
        "sentiment_score": 0.85,
        "sentiment_label": "POSITIVE",
        "entities": [{"text": "Tech Stocks", "label": "ORG"}],
    }

    # Act
    processed = ProcessedArticle.model_validate(data)

    # Assert
    assert processed.title == "Tech Stocks Rally"
    assert processed.sentiment_score == 0.85
    assert processed.sentiment_label == "POSITIVE"
    assert len(processed.entities) == 1
    assert processed.entities[0]["label"] == "ORG"


def test_processed_article_missing_nlp_fields() -> None:
    # Arrange: Valid RawArticle fields, but missing NLP fields required by ProcessedArticle
    data = {
        "title": "Tech Stocks Rally",
        "link": "https://tech.example.com",
        "published_date": "2026-08-13",
        "author": "Tech Reporter",
        "summary": "Tech stocks are rallying again.",
        "source": "rss",
    }

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        ProcessedArticle.model_validate(data)

    assert "sentiment_score\n  Field required" in str(exc_info.value)
    assert "sentiment_label\n  Field required" in str(exc_info.value)
    assert "entities\n  Field required" in str(exc_info.value)
