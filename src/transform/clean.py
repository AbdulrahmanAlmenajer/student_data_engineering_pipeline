import pandas as pd

from src.logger import logger


def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean student data before validation and loading.
    """

    logger.info(
        "Starting data cleaning: %d rows",
        len(df)
    )

    df = df.copy()

    # Clean column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    logger.info("Column names cleaned")

    # Clean text columns
    text_columns = ["name", "city"]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

    logger.info("Text columns cleaned")

    # Convert numeric columns
    numeric_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance",
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    logger.info("Numeric columns converted")


    logger.info(
        "Data cleaning completed: %d rows",
        len(df)
    )

    return df