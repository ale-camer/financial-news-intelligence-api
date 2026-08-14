import pytest

from src.nlp.orchestrator import process_article, process_batch


@pytest.mark.asyncio
async def test_process_article() -> None:
    article_data = {
        "id": "1",
        "title": "Apple News",
        "text": "  <p>Tim Cook announced that Apple revenue grew by 200%!</p>  ",
    }

    result = await process_article(article_data)

    assert result["id"] == "1"
    assert result["title"] == "Apple News"
    assert result["cleaned_text"] == "Tim Cook announced that Apple revenue grew by 200%!"
    assert "content_hash" in result
    assert isinstance(result["content_hash"], str)
    assert result["sentiment_label"] in ("positive", "negative", "neutral")
    assert isinstance(result["sentiment_score"], float)

    # Check if entities were extracted
    entities = result["entities"]
    assert isinstance(entities, list)
    assert any(e["entity"] == "Tim Cook" for e in entities)


@pytest.mark.asyncio
async def test_process_article_empty_text() -> None:
    article_data = {"id": "2", "text": ""}

    result = await process_article(article_data)

    assert result["cleaned_text"] == ""
    assert result["sentiment_label"] == "neutral"
    assert result["entities"] == []


@pytest.mark.asyncio
async def test_process_batch() -> None:
    articles = [
        {"text": "Apple is doing great."},
        {"text": "The market crashed today."},
        {"text": "Google released a new product."},
    ]

    results = await process_batch(articles)

    assert len(results) == 3
    for res in results:
        assert "cleaned_text" in res
        assert "sentiment_label" in res
        assert "entities" in res
