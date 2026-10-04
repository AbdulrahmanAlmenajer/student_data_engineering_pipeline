import sqlite3
from pathlib import Path

import pandas as pd

from src.logger import logger


def load_to_sqlite(
    df: pd.DataFrame,
    db_path: str | Path,
) -> None:
    """
    Load student data into SQLite.
    """

    db_path = Path(db_path)

    db_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Loading data into SQLite: %s",
        db_path
    )

    connection = sqlite3.connect(
        db_path
    )

    try:
        df.to_sql(
            "students",
            connection,
            if_exists="replace",
            index=False
        )

        logger.info(
            "SQLite load completed: %d rows",
            len(df)
        )

    finally:
        connection.close()

        logger.info(
            "SQLite connection closed"
        )