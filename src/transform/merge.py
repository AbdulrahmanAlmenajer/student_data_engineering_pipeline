import pandas as pd

from src.logger import logger


SOURCE_PRIORITY = {
    "csv": 1,
    "api": 2,
    "mongodb": 3,
    "postgresql": 4,
}


def merge_student_data(
    valid_dataframes: list[tuple[str, pd.DataFrame]],
    rejected_dataframes: list[tuple[str, pd.DataFrame]],
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Merge valid and rejected DataFrames from multiple data sources.

    Source priority:
        PostgreSQL > MongoDB > API > CSV

    When the same student_id exists in multiple valid sources,
    the record from the highest-priority source is kept.
    """

    logger.info("Starting source data merge")

    # =========================
    # Merge VALID data
    # =========================

    valid_frames = []

    row_order = 0

    for source_name, df in valid_dataframes:
        source_df = df.copy()

        source_df["_source"] = source_name
        source_df["_priority"] = SOURCE_PRIORITY[source_name]

        # Preserve original source/row order
        source_df["_order"] = range(
            row_order,
            row_order + len(source_df),
        )

        row_order += len(source_df)

        valid_frames.append(source_df)

    if valid_frames:
        combined_valid = pd.concat(
            valid_frames,
            ignore_index=True,
        )

        # Highest-priority source wins duplicates
        combined_valid = (
            combined_valid
            .sort_values(
                "_priority",
                ascending=False,
            )
            .drop_duplicates(
                subset=["student_id"],
                keep="first",
            )
            .sort_values(
                "_order",
                ascending=True,
            )
            .reset_index(drop=True)
        )

        # Remove internal columns
        combined_valid = combined_valid.drop(
            columns=["_priority", "_order"]
        )

    else:
        combined_valid = pd.DataFrame()

    # =========================
    # Merge REJECTED data
    # =========================

    rejected_frames = []

    for source_name, df in rejected_dataframes:
        source_df = df.copy()

        rejected_frames.append(source_df)

    if rejected_frames:
        combined_rejected = pd.concat(
            rejected_frames,
            ignore_index=True,
        )
    else:
        combined_rejected = pd.DataFrame()

    logger.info(
        "Source data merge completed: %d valid, %d rejected",
        len(combined_valid),
        len(combined_rejected),
    )

    return combined_valid, combined_rejected