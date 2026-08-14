from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from src.schemas.article import ArticleResponse
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
