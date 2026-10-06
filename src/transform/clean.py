import re

import numpy as np
import pandas as pd

from src.logger import logger


def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean student data before validation and loading.

    Cleaning steps:
        1. Standardize column names (strip, lowercase)
        2. Remove full duplicate rows
        3. Clean text columns (strip, capitalize, remove special characters)
        4. Convert numeric columns (coerce errors to NaN)
        5. Fill missing numeric values (age/attendance -> median, gpa -> mean)
        6. Fill missing text values (city -> mode)
        7. Cap outliers using IQR method (age, gpa, attendance)
        8. Round numeric columns to appropriate precision
        9. Generate and log a cleaning report
    """

    logger.info(
        "Starting data cleaning: %d rows",
        len(df)
    )

    df = df.copy()

    report = {}

    # =============================================
    # Step 1: Standardize column names
    # =============================================

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )

    logger.info("Column names standardized")

    # =============================================
    # Step 2: Remove full duplicate rows
    # =============================================

    duplicates_count = df.duplicated().sum()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    report["full_duplicates_removed"] = int(
        duplicates_count
    )

    logger.info(
        "Full duplicate rows removed: %d",
        duplicates_count
    )

    # =============================================
    # Step 3: Clean text columns
    # =============================================

    text_columns = ["name", "city"]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype("string")
                .str.strip()
            )

            # Remove special characters but keep
            # Arabic letters, English letters, spaces
            df[column] = df[column].apply(
                lambda x: _clean_text(x)
                if pd.notna(x) and x != ""
                else x
            )

            # Capitalize each word
            df[column] = df[column].apply(
                lambda x: x.title()
                if pd.notna(x) and x != ""
                else x
            )

    logger.info("Text columns cleaned and standardized")

    # =============================================
    # Step 4: Convert numeric columns
    # =============================================

    numeric_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance",
    ]

    for column in numeric_columns:
        if column in df.columns:
            original_nulls = df[column].isna().sum()

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

            new_nulls = df[column].isna().sum()
            coerced = int(new_nulls - original_nulls)

            if coerced > 0:
                report[f"{column}_coerced_to_nan"] = coerced
                logger.info(
                    "Column '%s': %d invalid values "
                    "coerced to NaN",
                    column,
                    coerced
                )

    logger.info("Numeric columns converted")

    # =============================================
    # Step 5: Fill missing numeric values
    # =============================================

    # Age -> median (robust to outliers)
    if "age" in df.columns:
        age_missing = int(df["age"].isna().sum())
        if age_missing > 0:
            age_median = df["age"].median()
            df["age"] = df["age"].fillna(age_median)

            report["age_missing_filled"] = age_missing
            report["age_fill_value_median"] = (
                round(float(age_median), 1)
            )

            logger.info(
                "Age: %d missing values filled "
                "with median = %.1f",
                age_missing,
                age_median
            )

    # GPA -> mean (sensitive to distribution)
    if "gpa" in df.columns:
        gpa_missing = int(df["gpa"].isna().sum())
        if gpa_missing > 0:
            gpa_mean = df["gpa"].mean()
            df["gpa"] = df["gpa"].fillna(gpa_mean)

            report["gpa_missing_filled"] = gpa_missing
            report["gpa_fill_value_mean"] = (
                round(float(gpa_mean), 2)
            )

            logger.info(
                "GPA: %d missing values filled "
                "with mean = %.2f",
                gpa_missing,
                gpa_mean
            )

    # Attendance -> median (robust to outliers)
    if "attendance" in df.columns:
        att_missing = int(
            df["attendance"].isna().sum()
        )
        if att_missing > 0:
            att_median = df["attendance"].median()
            df["attendance"] = df["attendance"].fillna(
                att_median
            )

            report["attendance_missing_filled"] = (
                att_missing
            )
            report["attendance_fill_value_median"] = (
                round(float(att_median), 1)
            )

            logger.info(
                "Attendance: %d missing values filled "
                "with median = %.1f",
                att_missing,
                att_median
            )

    # =============================================
    # Step 6: Fill missing text values
    # =============================================

    if "city" in df.columns:
        city_missing = int(
            df["city"].isna().sum()
            + df["city"].eq("").sum()
        )

        if city_missing > 0:
            city_mode = _get_mode(df, "city")

            if city_mode is not None:
                df["city"] = df["city"].replace(
                    "", pd.NA
                )
                df["city"] = df["city"].fillna(
                    city_mode
                )

                report["city_missing_filled"] = (
                    city_missing
                )
                report["city_fill_value_mode"] = (
                    city_mode
                )

                logger.info(
                    "City: %d missing values filled "
                    "with mode = '%s'",
                    city_missing,
                    city_mode
                )

    # =============================================
    # Step 7: Cap outliers using IQR method
    # =============================================

    outlier_columns = {
        "age": {"lower": 15, "upper": 100},
        "gpa": {"lower": 0.0, "upper": 4.0},
        "attendance": {"lower": 0, "upper": 100},
    }

    for column, bounds in outlier_columns.items():
        if column in df.columns:
            outliers_capped = _cap_outliers_iqr(
                df, column, bounds
            )

            if outliers_capped > 0:
                report[
                    f"{column}_outliers_capped"
                ] = outliers_capped

    # =============================================
    # Step 8: Round numeric columns
    # =============================================

    if "age" in df.columns:
        df["age"] = df["age"].round(0).astype(
            "Int64"
        )

    if "gpa" in df.columns:
        df["gpa"] = df["gpa"].round(2)

    if "attendance" in df.columns:
        df["attendance"] = (
            df["attendance"].round(1)
        )

    if "student_id" in df.columns:
        df["student_id"] = (
            df["student_id"]
            .round(0)
            .astype("Int64")
        )

    logger.info("Numeric columns rounded")

    # =============================================
    # Step 9: Log cleaning report
    # =============================================

    _log_cleaning_report(df, report)

    logger.info(
        "Data cleaning completed: %d rows",
        len(df)
    )

    return df


# =================================================
# Helper Functions
# =================================================


def _clean_text(text: str) -> str:
    """
    Remove special characters from text.
    Keep Arabic letters, English letters, spaces,
    and basic punctuation.
    """

    if pd.isna(text) or text == "":
        return text

    # Keep Arabic, English, numbers, spaces,
    # hyphens, and dots
    cleaned = re.sub(
        r"[^\u0600-\u06FF\u0750-\u077F"
        r"a-zA-Z0-9\s.\-]",
        "",
        str(text)
    )

    # Collapse multiple spaces into one
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    return cleaned


def _get_mode(
    df: pd.DataFrame,
    column: str,
) -> str | None:
    """
    Get the mode of a text column,
    ignoring empty strings and NaN.
    """

    valid_values = df[column].replace("", pd.NA)
    valid_values = valid_values.dropna()

    if valid_values.empty:
        return None

    mode = valid_values.mode()

    if mode.empty:
        return None

    return str(mode.iloc[0])


def _cap_outliers_iqr(
    df: pd.DataFrame,
    column: str,
    bounds: dict,
) -> int:
    """
    Cap outliers using IQR method combined
    with domain bounds.

    Uses the tighter of IQR-based limits and
    domain-specific bounds.

    Returns the number of values capped.
    """

    valid_data = df[column].dropna()

    if valid_data.empty:
        return 0

    q1 = valid_data.quantile(0.25)
    q3 = valid_data.quantile(0.75)
    iqr = q3 - q1

    # IQR-based bounds
    iqr_lower = q1 - 1.5 * iqr
    iqr_upper = q3 + 1.5 * iqr

    # Use the tighter of IQR and domain bounds
    effective_lower = max(
        iqr_lower, bounds["lower"]
    )
    effective_upper = min(
        iqr_upper, bounds["upper"]
    )

    below = df[column] < effective_lower
    above = df[column] > effective_upper

    outlier_count = int(
        below.sum() + above.sum()
    )

    if outlier_count > 0:
        df[column] = df[column].clip(
            lower=effective_lower,
            upper=effective_upper
        )

        logger.info(
            "Column '%s': %d outliers capped "
            "to range [%.2f, %.2f]",
            column,
            outlier_count,
            effective_lower,
            effective_upper
        )

    return outlier_count


def _log_cleaning_report(
    df: pd.DataFrame,
    report: dict,
) -> None:
    """
    Log a summary cleaning report with
    descriptive statistics.
    """

    logger.info("=" * 50)
    logger.info("DATA CLEANING REPORT")
    logger.info("=" * 50)

    logger.info(
        "Final row count: %d",
        len(df)
    )

    # Report actions taken
    if report:
        logger.info("--- Actions Taken ---")
        for key, value in report.items():
            logger.info("  %s: %s", key, value)

    # Descriptive statistics for numeric columns
    numeric_cols = ["age", "gpa", "attendance"]
    available_cols = [
        col for col in numeric_cols
        if col in df.columns
    ]

    if available_cols:
        logger.info(
            "--- Descriptive Statistics ---"
        )

        for col in available_cols:
            valid_data = pd.to_numeric(
                df[col], errors="coerce"
            ).dropna()

            if valid_data.empty:
                logger.info(
                    "  %s: no valid data", col
                )
                continue

            std_val = valid_data.std()
            if pd.isna(std_val):
                std_val = 0.0

            stats = {
                "count": int(valid_data.count()),
                "mean": round(
                    float(valid_data.mean()), 2
                ),
                "median": round(
                    float(valid_data.median()), 2
                ),
                "std": round(
                    float(std_val), 2
                ),
                "min": round(
                    float(valid_data.min()), 2
                ),
                "max": round(
                    float(valid_data.max()), 2
                ),
                "q1": round(
                    float(
                        valid_data.quantile(0.25)
                    ),
                    2
                ),
                "q3": round(
                    float(
                        valid_data.quantile(0.75)
                    ),
                    2
                ),
            }

            logger.info(
                "  %s -> count=%d, mean=%.2f, "
                "median=%.2f, std=%.2f, "
                "min=%.2f, max=%.2f, "
                "Q1=%.2f, Q3=%.2f",
                col,
                stats["count"],
                stats["mean"],
                stats["median"],
                stats["std"],
                stats["min"],
                stats["max"],
                stats["q1"],
                stats["q3"],
            )

    # Missing values summary
    missing = df.isna().sum()
    total_missing = int(missing.sum())

    logger.info(
        "--- Remaining Missing Values ---"
    )

    if total_missing == 0:
        logger.info(
            "  No missing values remaining"
        )
    else:
        for col_name in missing.index:
            if missing[col_name] > 0:
                logger.info(
                    "  %s: %d missing",
                    col_name,
                    int(missing[col_name])
                )

    logger.info("=" * 50)