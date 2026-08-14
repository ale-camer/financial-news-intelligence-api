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
    entities: list[dict[str, Any]]


class ArticleResponse(RawArticle):
    """
    Schema for article API responses including database ID and optional NLP fields.
    """

    id: int
    sentiment_score: float | None = None
    sentiment_label: str | None = None
    entities: list[dict[str, Any]] | None = None

    model_config = {"from_attributes": True}


class ArticleSentimentResponse(BaseModel):
    """
    Schema for detailed sentiment and NLP response of a specific article.
    """

    id: int
    sentiment_score: float | None = None
    sentiment_label: str | None = None
    entities: list[dict[str, Any]] | None = None

    model_config = {"from_attributes": True}
