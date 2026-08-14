from typing import cast
from unittest.mock import MagicMock

from bson import ObjectId

from src.storage.mongodb import ArticleRepository, get_mongo_client


def test_get_mongo_client() -> None:
    client = get_mongo_client("mongodb://localhost:27017")
    assert client is not None


def test_article_repository_create_indexes() -> None:
    mock_client = MagicMock()
    repo = ArticleRepository(client=mock_client, db_name="test_db")
    repo.create_indexes()

    mock_collection = cast(MagicMock, repo.collection)
    assert mock_collection.create_index.call_count == 3


def test_article_repository_save_article() -> None:
    mock_client = MagicMock()
    mock_insert_result = MagicMock()
    dummy_oid = ObjectId()
    mock_insert_result.inserted_id = dummy_oid
    mock_client["test_db"]["articles"].insert_one.return_value = mock_insert_result

    repo = ArticleRepository(client=mock_client, db_name="test_db")
    doc = {"title": "Test Article", "link": "https://example.com/test"}
    oid_str = repo.save_article(doc)

    assert oid_str == str(dummy_oid)
    mock_client["test_db"]["articles"].insert_one.assert_called_once_with(doc)


def test_article_repository_get_article_by_id_success() -> None:
    mock_client = MagicMock()
    dummy_oid = ObjectId()
    doc_in_db = {"_id": dummy_oid, "title": "Test Article"}
    mock_client["test_db"]["articles"].find_one.return_value = doc_in_db

    repo = ArticleRepository(client=mock_client, db_name="test_db")
    result = repo.get_article_by_id(str(dummy_oid))

    assert result is not None
    assert result["_id"] == str(dummy_oid)
    assert result["title"] == "Test Article"


def test_article_repository_get_article_by_id_invalid_oid() -> None:
    mock_client = MagicMock()
    mock_client["test_db"]["articles"].find_one.return_value = None

    repo = ArticleRepository(client=mock_client, db_name="test_db")
    result = repo.get_article_by_id("non_existent_string_id")

    assert result is None
    mock_client["test_db"]["articles"].find_one.assert_called_once_with(
        {"_id": "non_existent_string_id"}
    )


def test_article_repository_list_articles() -> None:
    mock_client = MagicMock()
    dummy_oid = ObjectId()
    doc_in_db = {"_id": dummy_oid, "title": "Test Article"}

    mock_cursor = MagicMock()
    mock_cursor.skip.return_value = mock_cursor
    mock_cursor.limit.return_value = mock_cursor
    mock_cursor.__iter__.return_value = iter([doc_in_db])

    mock_client["test_db"]["articles"].find.return_value = mock_cursor

    repo = ArticleRepository(client=mock_client, db_name="test_db")
    articles = repo.list_articles({"source": "rss"}, skip=0, limit=10)

    assert len(articles) == 1
    assert articles[0]["_id"] == str(dummy_oid)
    mock_client["test_db"]["articles"].find.assert_called_once_with({"source": "rss"})


def test_article_repository_delete_article_success() -> None:
    mock_client = MagicMock()
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 1
    mock_client["test_db"]["articles"].delete_one.return_value = mock_delete_result

    repo = ArticleRepository(client=mock_client, db_name="test_db")
    dummy_oid = ObjectId()
    success = repo.delete_article(str(dummy_oid))

    assert success is True


def test_article_repository_delete_article_not_found() -> None:
    mock_client = MagicMock()
    mock_delete_result = MagicMock()
    mock_delete_result.deleted_count = 0
    mock_client["test_db"]["articles"].delete_one.return_value = mock_delete_result

    repo = ArticleRepository(client=mock_client, db_name="test_db")
    success = repo.delete_article("non_existent_id")

    assert success is False
