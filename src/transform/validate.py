import pandas as pd

from src.logger import logger
def add_rejection_reason(
    df: pd.DataFrame,
    mask: pd.Series,
    reason: str,
) -> None:
    df.loc[
        mask,
        "rejection_reason"
    ] = (
        df.loc[
            mask,
            "rejection_reason"
        ]
        .replace("", pd.NA)
        .fillna("")
        .apply(
            lambda x: (
                reason
                if x == ""
                else f"{x}; {reason}"
            )
        )
    )


def validate_students(df: pd.DataFrame,) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Validate student data.

    Returns:
        valid_df: valid student records
        rejected_df: rejected records with rejection reasons
    """

    logger.info(
        "Starting data validation: %d rows",
        len(df)
    )
    df = df.copy()

    df["rejection_reason"] = ""
    missing_student_id = df["student_id"].isna()

    add_rejection_reason(
        df,
        missing_student_id,
        "missing student_id"
    )
    logger.warning(
        "Missing student_id: %d",
        missing_student_id.sum()
    )
    duplicate_student_id = (
        df["student_id"].duplicated(
            keep=False
        )
        & df["student_id"].notna()
    )
    add_rejection_reason(
        df,
        duplicate_student_id,
        "duplicate student_id"
    )
    logger.warning(
        "Duplicate student_id records: %d",
        duplicate_student_id.sum()
    )
    missing_name = (
        df["name"].isna()
        | df["name"].eq("")
    )

    add_rejection_reason(
        df,
        missing_name,
        "missing name"
    )

    logger.warning(
        "Missing name: %d",
        missing_name.sum()
    )
    invalid_age = (
        df["age"].isna()
        | (df["age"] < 15)
        | (df["age"] > 100)
    )

    add_rejection_reason(
        df,
        invalid_age,
        "invalid age"
    )

    logger.warning(
        "Invalid age: %d",
        invalid_age.sum()
    )
    invalid_gpa = (
        df["gpa"].isna()
        | (df["gpa"] < 0)
        | (df["gpa"] > 4)
    )

    add_rejection_reason(
        df,
        invalid_gpa,
        "invalid gpa"
    )

    logger.warning(
        "Invalid GPA: %d",
        invalid_gpa.sum()
    )
    invalid_attendance = (
        df["attendance"].isna()
        | (df["attendance"] < 0)
        | (df["attendance"] > 100)
    )

    add_rejection_reason(
        df,
        invalid_attendance,
        "invalid attendance"
    )

    logger.warning(
        "Invalid attendance: %d",
        invalid_attendance.sum()
    )
    missing_city = (
        df["city"].isna()
        | df["city"].eq("")
    )

    add_rejection_reason(
        df,
        missing_city,
        "missing city"
    )

    logger.warning(
        "Missing city: %d",
        missing_city.sum()
    )
    rejected_mask = (
            df["rejection_reason"] != ""
    )

    valid_df = df[
        ~rejected_mask
    ].copy()

    rejected_df = df[
        rejected_mask
    ].copy()

    logger.info(
        "Valid records: %d",
        len(valid_df)
    )

    logger.warning(
        "Rejected records: %d",
        len(rejected_df)
    )

    logger.info(
        "Data validation completed"
    )

    return valid_df, rejected_df