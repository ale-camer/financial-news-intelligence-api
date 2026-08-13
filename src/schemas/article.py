from typing import Any

from pydantic import BaseModel


class RawArticle(BaseModel):
    """
    Schema representing a raw article ingested from sources like RSS or NewsAPI.
    """

    title: str
    link: str  # We use str here to be flexible, but it could be HttpUrl
    published_date: str
    author: str
    summary: str
    source: str


class ProcessedArticle(RawArticle):
    """
    Schema representing an article after NLP processing has been applied.
    Inherits all fields from RawArticle and adds sentiment and entities.
    """

    sentiment_score: float
    sentiment_label: str
    # Entities could be a list of strings or list of dicts.
    # We use List[Dict[str, Any]] as a flexible structure for NER outputs like:
    # [{"text": "Apple", "label": "ORG"}, {"text": "Tim Cook", "label": "PERSON"}]
    entities: list[dict[str, Any]]
