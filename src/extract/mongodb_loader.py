import pandas as pd
from pymongo import MongoClient

from src.logger import logger


def load_mongodb(
    uri: str,
    database_name: str,
    collection_name: str,
) -> pd.DataFrame:
    """
    Load student data from MongoDB.
    """

    logger.info(
        "Starting MongoDB extraction: %s.%s",
        database_name,
        collection_name
    )

    client = MongoClient(uri)

    try:
        collection = client[
            database_name
        ][
            collection_name
        ]

        documents = list(
            collection.find(
                {},
                {"_id": 0}
            )
        )

        df = pd.DataFrame(documents)

        logger.info(
            "MongoDB loaded successfully: %d rows, %d columns",
            len(df),
            len(df.columns)
        )

        return df

    finally:
        client.close()

        logger.info(
            "MongoDB connection closed"
        )