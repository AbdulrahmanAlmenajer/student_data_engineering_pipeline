import pandas as pd
from pymongo import MongoClient

from src.logger import logger


def load_mongodb(
    uri: str,
    database_name: str,
    collection_name: str,
) -> pd.DataFrame:
    """
    Load student data from MongoDB
    using the standard student schema.
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
                {
                    "_id": 0,
                    "student_id": 1,
                    "name": 1,
                    "age": 1,
                    "gpa": 1,
                    "attendance": 1,
                    "city": 1,
                }
            )
        )

        df = pd.DataFrame(documents)

        required_columns = [
            "student_id",
            "name",
            "age",
            "gpa",
            "attendance",
            "city",
        ]

        # Ensure all standard columns exist
        for column in required_columns:
            if column not in df.columns:
                df[column] = pd.NA

        # Keep only the standard student schema
        df = df[required_columns]

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