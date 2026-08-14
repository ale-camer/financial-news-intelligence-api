from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from src.schemas.article import ArticleResponse, ArticleSentimentResponse
from src.storage.db import get_session
from src.storage.models import Article

router = APIRouter()


@router.get("/", response_model=list[ArticleResponse])
def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    source: str | None = Query(None),
    sentiment_label: str | None = Query(None),
    session: Session = Depends(get_session),
) -> Any:
    """
    Retrieve articles with optional pagination and filtering.
    """
    query = session.query(Article)

    if source:
        query = query.filter(Article.source == source)
    if sentiment_label:
        query = query.filter(Article.sentiment_label == sentiment_label)

    articles = query.offset(skip).limit(limit).all()
    return articles


@router.get("/{article_id}/sentiment", response_model=ArticleSentimentResponse)
def get_article_sentiment(
    article_id: int = Path(..., title="The ID of the article", ge=1),
    session: Session = Depends(get_session),
) -> Any:
    """
    Retrieve detailed sentiment and NER insights for a single article.
    """
    article = session.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
