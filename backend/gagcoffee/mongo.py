"""
MongoDB connection singleton.
Usage:
    from gagcoffee.mongo import db
    db.orders.insert_one({...})
"""
from pymongo import MongoClient
from django.conf import settings

_client: MongoClient | None = None


def get_client() -> MongoClient:
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI)
    return _client


def get_db():
    return get_client()[settings.MONGODB_DB]


# Convenient shorthand ─ import and use as `db.orders`, `db.contacts` etc.
class _DB:
    def __getattr__(self, name):
        return get_db()[name]


db = _DB()
