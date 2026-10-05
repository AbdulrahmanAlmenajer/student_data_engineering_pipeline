
import pandas as pd

from src.logger import logger


def merge_student_data(
    valid_dataframes: list[pd.DataFrame],
    rejected_dataframes: list[pd.DataFrame],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Merge valid and rejected DataFrames
    from multiple data sources.

    Args:
        valid_dataframes:
            List of valid DataFrames.

        rejected_dataframes:
            List of rejected DataFrames.

    Returns:
        combined_valid:
            Combined valid student records.

        combined_rejected:
            Combined rejected student records.
    """

    logger.info(
        "Starting source data merge"
    )

    combined_valid = pd.concat(
        valid_dataframes,
        ignore_index=True,
    )

    combined_rejected = pd.concat(
        rejected_dataframes,
        ignore_index=True,
    )

    logger.info(
        "Source data merge completed: "
        "%d valid, %d rejected",
        len(combined_valid),
        len(combined_rejected),
    )

    return (
        combined_valid,
        combined_rejected,
    )
