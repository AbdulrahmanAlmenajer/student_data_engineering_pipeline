import pandas as pd

from src.logger import logger
from src.transform.clean import clean_students
from src.transform.validate import validate_students


def process_students(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Clean and validate student data.

    Returns:
        valid_df: valid student records
        rejected_df: rejected student records
    """

    logger.info(
        "Starting student data processing: %d rows",
        len(df)
    )

    cleaned_df = clean_students(df)

    valid_df, rejected_df = validate_students(
        cleaned_df
    )

    logger.info(
        "Student data processing completed: %d valid, %d rejected",
        len(valid_df),
        len(rejected_df)
    )

    return valid_df, rejected_df