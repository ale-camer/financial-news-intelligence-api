from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.api.config import settings
from src.ingestion.orchestrator import run_ingestion
from src.nlp.orchestrator import process_batch
from src.schemas.article import ProcessedArticle
from src.storage.db import get_session
from src.storage.models import Article

router = APIRouter()


@router.post("/trigger")
async def trigger_ingestion(session: Session = Depends(get_session)) -> dict[str, Any]:
    """
    Trigger the ingestion and NLP processing pipelines.
    Fetches raw articles, processes them through NLP, and saves them to the DB.
    """
    rss_urls = [
        "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",
        "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664",
    ]

    # 1. Ingestion (M1)
    raw_articles = await run_ingestion(
        newsapi_key=settings.NEWSAPI_KEY,
        newsapi_query="finance",
        rss_urls=rss_urls,
    )

    if not raw_articles:
        return {"status": "success", "articles_processed": 0, "articles_saved": 0}

    # 2. Convert to dicts for NLP orchestrator
    article_dicts = [article.model_dump() for article in raw_articles]

    # 3. NLP Processing (M2)
    processed_dicts = await process_batch(article_dicts)

    # Validate processed dicts and map to DB models
    saved_count = 0
    for data in processed_dicts:
        try:
            processed_model = ProcessedArticle.model_validate(data)

            db_article = Article(
                title=processed_model.title,
                link=processed_model.link,
                published_date=processed_model.published_date,
                author=processed_model.author,
                summary=processed_model.summary,
                source=processed_model.source,
                sentiment_score=processed_model.sentiment_score,
                sentiment_label=processed_model.sentiment_label,
                entities=processed_model.entities,
            )
            session.add(db_article)
            session.commit()
            saved_count += 1
        except IntegrityError:
            session.rollback()  # Duplicate link
        except Exception:
            session.rollback()

    return {
        "status": "success",
        "articles_processed": len(processed_dicts),
        "articles_saved": saved_count,
    }
