import pandas as pd

from src.extract.csv_loader import load_csv
from src.extract.mongodb_loader import load_mongodb
from src.pipeline import process_students


def test_combine_csv_and_mongodb():
    """Integration test: combine CSV and MongoDB
    data through the full pipeline.

    With the enhanced cleaner, more records pass
    validation because missing values are filled
    and outliers are capped.
    """

    # Extract CSV
    csv_df = load_csv(
        "data/raw/students.csv"
    )

    # Extract MongoDB
    mongodb_df = load_mongodb(
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )

    # Process CSV
    csv_valid, csv_rejected = process_students(
        csv_df
    )

    # Process MongoDB
    mongo_valid, mongo_rejected = process_students(
        mongodb_df
    )

    # Combine valid data
    combined_valid = pd.concat(
        [
            csv_valid,
            mongo_valid,
        ],
        ignore_index=True,
    )

    # Combine rejected data
    combined_rejected = pd.concat(
        [
            csv_rejected,
            mongo_rejected,
        ],
        ignore_index=True,
    )

    # Ensure we have data from both sources
    assert len(combined_valid) > 0
    assert len(csv_valid) > 0
    assert len(mongo_valid) > 0

    # Total should match original inputs
    # minus full duplicates
    total_processed = (
        len(combined_valid)
        + len(combined_rejected)
    )
    assert total_processed > 0

    # Check standard schema
    expected_columns = [
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    ]

    assert list(
        combined_valid.drop(
            columns=["rejection_reason"]
        ).columns
    ) == expected_columns

    if len(combined_rejected) > 0:
        assert list(
            combined_rejected.drop(
                columns=["rejection_reason"]
            ).columns
        ) == expected_columns


    print("\n===== COMBINED VALID STUDENT IDs =====")
    print(
        combined_valid[
            ["student_id", "name", "city"]
        ]
    )