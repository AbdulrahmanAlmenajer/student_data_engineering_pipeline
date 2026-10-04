from pathlib import Path

import pandas as pd

from src.logger import logger


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """
    Load student data from a CSV file.
    """

    file_path = Path(file_path)

    logger.info(
        "Starting CSV extraction: %s",
        file_path
    )

    if not file_path.exists():
        logger.error(
            "CSV file not found: %s",
            file_path
        )

        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    logger.info(
        "CSV loaded successfully: %d rows, %d columns",
        len(df),
        len(df.columns)
    )

    return df