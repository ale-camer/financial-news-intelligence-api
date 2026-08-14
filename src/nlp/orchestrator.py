import asyncio
from typing import Any

from src.nlp.ner import extract_entities
from src.nlp.preprocessing import clean_text, generate_content_hash
from src.nlp.sentiment import analyze_sentiment


async def process_article(article_data: dict[str, str]) -> dict[str, Any]:
    """
    Process a single article through the NLP pipeline.

    Args:
        article_data: A dictionary containing the article data. Must have a 'text' key.

    Returns:
        A new dictionary with the original data plus enriched NLP fields.
    """
    raw_text = article_data.get("text", "")
    cleaned_text = clean_text(raw_text)
    content_hash = generate_content_hash(cleaned_text)

    # Run CPU-bound ML tasks concurrently in separate threads
    sentiment_task = asyncio.to_thread(analyze_sentiment, cleaned_text)
    entities_task = asyncio.to_thread(extract_entities, cleaned_text)

    sentiment_result, entities_result = await asyncio.gather(sentiment_task, entities_task)
    sentiment_label, sentiment_score = sentiment_result

    result: dict[str, Any] = {**article_data}
    result.update(
        {
            "cleaned_text": cleaned_text,
            "content_hash": content_hash,
            "sentiment_label": sentiment_label,
            "sentiment_score": sentiment_score,
            "entities": entities_result,
        }
    )

    return result


async def process_batch(articles: list[dict[str, str]]) -> list[dict[str, Any]]:
    """
    Process a batch of articles concurrently through the NLP pipeline.

    Args:
        articles: A list of article data dictionaries.

    Returns:
        A list of enriched article data dictionaries.
    """
    tasks = [process_article(article) for article in articles]
    return await asyncio.gather(*tasks)
