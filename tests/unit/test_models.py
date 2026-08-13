from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.storage.models import Article, Base


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Creates an in-memory SQLite database and yields a SQLAlchemy session.
    The database is destroyed after the test finishes.
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


def test_article_model_instantiation() -> None:
    # Arrange & Act
    article = Article(
        title="Test Title",
        link="https://test.com/article1",
        published_date="2026-08-13",
        author="John Doe",
        summary="Test Summary",
        source="rss",
        sentiment_score=0.9,
        sentiment_label="POSITIVE",
        entities=[{"text": "Apple", "label": "ORG"}],
    )

    # Assert basic attributes are set correctly
    assert article.title == "Test Title"
    assert article.sentiment_score == 0.9


def test_article_database_insert_and_query(db_session: Session) -> None:
    # Arrange
    article = Article(
        title="DB Test",
        link="https://dbtest.com",
        published_date="2026-08-13",
        author="Jane Doe",
        summary="Saved to DB",
        source="newsapi",
        entities=[{"text": "Google", "label": "ORG"}],
    )

    # Act
    db_session.add(article)
    db_session.commit()

    # Query it back
    saved_article = db_session.query(Article).filter_by(title="DB Test").first()

    # Assert
    assert saved_article is not None
    assert saved_article.id == 1
    assert saved_article.link == "https://dbtest.com"

    # Test that JSON field serializes/deserializes correctly
    assert isinstance(saved_article.entities, list)
    if saved_article.entities:
        assert saved_article.entities[0]["text"] == "Google"


def test_article_unique_link_constraint(db_session: Session) -> None:
    # Arrange
    article1 = Article(
        title="Article 1",
        link="https://unique.com",
        published_date="2026-08-13",
        author="Author A",
        summary="Summary 1",
        source="rss",
    )

    article2 = Article(
        title="Article 2",
        link="https://unique.com",  # Duplicate link
        published_date="2026-08-14",
        author="Author B",
        summary="Summary 2",
        source="newsapi",
    )

    # Act & Assert
    db_session.add(article1)
    db_session.commit()

    db_session.add(article2)
    with pytest.raises(IntegrityError):
        db_session.commit()
