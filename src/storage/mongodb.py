from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.api.config import settings


def get_mongo_client(url: str | None = None) -> MongoClient[dict[str, Any]]:
    """
    Get PyMongo client instance.
    """
    mongo_url = url or settings.MONGODB_URL
    return MongoClient(mongo_url)


class ArticleRepository:
    """
    Repository layer for managing article document storage in MongoDB.
    """

    def __init__(
        self,
        client: MongoClient[dict[str, Any]] | None = None,
        db_name: str | None = None,
    ) -> None:
        self.client = client or get_mongo_client()
        self.db: Database[dict[str, Any]] = self.client[db_name or settings.MONGODB_DB_NAME]
        self.collection: Collection[dict[str, Any]] = self.db["articles"]

    def create_indexes(self) -> None:
        """
        Create indexes for link, published_date, and sentiment_label.
        """
        self.collection.create_index("link", unique=True)
        self.collection.create_index([("published_date", -1)])
        self.collection.create_index([("sentiment_label", 1)])

    def save_article(self, article_data: dict[str, Any]) -> str:
        """
        Insert an article document into MongoDB.
        Returns the string representation of the inserted ObjectId.
        """
        result = self.collection.insert_one(article_data)
        return str(result.inserted_id)

    def get_article_by_id(self, article_id: str) -> dict[str, Any] | None:
        """
        Retrieve an article by string representation of ObjectId or string ID.
        """
        try:
            doc_id: Any = ObjectId(article_id)
        except InvalidId:
            doc_id = article_id

        doc = self.collection.find_one({"_id": doc_id})
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    def list_articles(
        self,
        filter_query: dict[str, Any] | None = None,
        skip: int = 0,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        """
        List articles with optional filtering and pagination.
        """
        query = filter_query or {}
        cursor = self.collection.find(query).skip(skip).limit(limit)
        results: list[dict[str, Any]] = []
        for doc in cursor:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            results.append(doc)
        return results

    def delete_article(self, article_id: str) -> bool:
        """
        Delete an article document by ID.
        """
        try:
            doc_id: Any = ObjectId(article_id)
        except InvalidId:
            doc_id = article_id

        result = self.collection.delete_one({"_id": doc_id})
        return result.deleted_count > 0
