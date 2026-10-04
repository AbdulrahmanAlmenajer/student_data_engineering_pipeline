from pathlib import Path

import pandas as pd

from src.logger import logger


def save_csv(
    df: pd.DataFrame,
    file_path: str | Path,
) -> None:
    """
    Save a DataFrame to a CSV file.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        "Saving CSV: %s",
        file_path
    )

    df.to_csv(
        file_path,
        index=False,
        encoding="utf-8"
    )

    logger.info(
        "CSV saved successfully: %d rows",
        len(df)
    )