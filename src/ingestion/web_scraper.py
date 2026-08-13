import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def scrape_article_text(url: str) -> str:
    """
    Fetches the HTML content of the given URL and extracts the main text.
    Uses BeautifulSoup to parse paragraph tags.

    Args:
        url (str): The URL of the article to scrape.

    Returns:
        str: The extracted plain text of the article. Returns an empty string
        if the request fails or parsing errors occur.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Extract text from all paragraph tags.
        # This is a basic but effective approach for most news articles.
        paragraphs = soup.find_all("p")

        text_fragments = []
        for p in paragraphs:
            # Use separator=" " to avoid squashing words together when stripping tags
            text = p.get_text(separator=" ", strip=True)
            if text:
                text_fragments.append(text)

        return " ".join(text_fragments)

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while scraping {url}: {e}")
        return ""
    except Exception as e:
        logger.error(f"Unexpected error while parsing {url}: {e}")
        return ""
