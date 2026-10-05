import pandas as pd

from src.extract.csv_loader import load_csv
from src.extract.mongodb_loader import load_mongodb
from src.pipeline import process_students


def test_combine_csv_and_mongodb():

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

    # Check total counts
    assert len(combined_valid) == 7
    assert len(combined_rejected) == 21

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