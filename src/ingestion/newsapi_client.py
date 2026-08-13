import logging
from typing import Any

import requests

logger = logging.getLogger(__name__)


def fetch_newsapi_feed(query: str, api_key: str) -> list[dict[str, Any]]:
    """
    Fetches and parses financial news from the NewsAPI service.

    Args:
        query (str): The search query (e.g., 'finance' or 'AAPL').
        api_key (str): The NewsAPI key for authentication.

    Returns:
        list[dict[str, Any]]: A list of normalized news items containing
        title, link, published_date, author, and summary.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": api_key,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        articles = data.get("articles", [])

        items = []
        for article in articles:
            # NewsAPI sometimes returns articles that have been removed
            if article.get("title") == "[Removed]":
                continue

            item = {
                "title": article.get("title", "") or "",
                "link": article.get("url", "") or "",
                "published_date": article.get("publishedAt", "") or "",
                "author": article.get("author", "") or "",
                "summary": article.get("description", "") or "",
            }
            items.append(item)

        return items

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching NewsAPI feed for query '{query}': {e}")
        return []
    except ValueError as e:
        logger.error(f"Error parsing JSON response from NewsAPI: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while fetching NewsAPI feed for query '{query}': {e}")
        return []
