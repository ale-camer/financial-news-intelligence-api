import logging
from typing import Any

import feedparser
import requests

logger = logging.getLogger(__name__)


def fetch_rss_feed(url: str) -> list[dict[str, Any]]:
    """
    Fetches and parses an RSS feed from the given URL.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        List[Dict[str, Any]]: A list of normalized news items containing
        title, link, published_date, author, and summary.
    """
    try:
        # Use a standard User-Agent header to avoid basic anti-scraping blocks (e.g., 429 errors from Yahoo)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        # Use requests to fetch the content with a timeout for better control
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse the feed content using feedparser
        feed = feedparser.parse(response.content)

        # feed.bozo is set to 1 if the feed is not well-formed XML
        if getattr(feed, "bozo", 0) == 1:
            logger.warning(
                f"Feedparser encountered an issue parsing {url}: {getattr(feed, 'bozo_exception', 'Unknown error')}"
            )

        items = []
        for entry in feed.entries:
            item = {
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published_date": entry.get("published", ""),
                "author": entry.get("author", ""),
                "summary": entry.get("summary", ""),
            }
            items.append(item)

        return items

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while fetching RSS feed from {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error while parsing RSS feed from {url}: {e}")
        return []
