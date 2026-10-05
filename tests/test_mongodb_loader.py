from pymongo import MongoClient


def test_mongodb_connection():
    client = MongoClient(
        "mongodb://localhost:27017/",
        serverSelectionTimeoutMS=2000,
    )

    try:
        client.admin.command("ping")

    finally:
        client.close()