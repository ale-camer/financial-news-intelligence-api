import asyncio
import logging

from pydantic import ValidationError

from src.ingestion.newsapi_client import fetch_newsapi_feed
from src.ingestion.rss_client import fetch_rss_feed
from src.schemas.article import RawArticle

logger = logging.getLogger(__name__)


async def run_ingestion(
    newsapi_key: str, newsapi_query: str, rss_urls: list[str]
) -> list[RawArticle]:
    """
    Asynchronously coordinates fetching from multiple RSS feeds and NewsAPI.
    Validates and transforms the raw dicts into RawArticle Pydantic models.
    """
    tasks = []

    # Add RSS tasks
    for url in rss_urls:
        tasks.append(asyncio.to_thread(fetch_rss_feed, url))

    # Add NewsAPI task
    tasks.append(asyncio.to_thread(fetch_newsapi_feed, newsapi_query, newsapi_key))

    # Execute all fetching tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    parsed_articles: list[RawArticle] = []

    for result in results:
        # If a task raised an exception, log it and continue
        if isinstance(result, BaseException):
            logger.error(f"Ingestion task failed with exception: {result}")
            continue

        # Parse successful dictionaries into RawArticle models
        for item in result:
            try:
                article = RawArticle.model_validate(item)
                parsed_articles.append(article)
            except ValidationError as e:
                logger.warning("Skipping corrupted article due to validation error")
                logger.debug(f"Validation error details: {e}")
                continue

    return parsed_articles
