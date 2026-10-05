import pandas as pd
from src.transform.clean import clean_students
from src.transform.validate import validate_students
from src.extract.mongodb_loader import load_mongodb


def test_load_mongodb():
    df = load_mongodb(
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )

    assert isinstance(df, pd.DataFrame)

    assert not df.empty

    required_columns = {
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    }

    assert required_columns.issubset(
        df.columns
    )



def test_mongodb_data_validation():
    df = load_mongodb(
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )

    cleaned_df = clean_students(df)

    valid_df, rejected_df = validate_students(
        cleaned_df
    )

    assert len(valid_df) > 0
    assert len(rejected_df) > 0

    assert "rejection_reason" in rejected_df.columns

    assert rejected_df[
        "rejection_reason"
    ].ne("").all()

def test_mongodb_data_quality_report():
    df = load_mongodb(
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )

    cleaned_df = clean_students(df)

    valid_df, rejected_df = validate_students(
        cleaned_df
    )

    print(
        f"\nMongoDB total records: {len(df)}"
    )

    print(
        f"MongoDB valid records: {len(valid_df)}"
    )

    print(
        f"MongoDB rejected records: {len(rejected_df)}"
    )

    if not rejected_df.empty:
        print(
            "\nRejection reasons:"
        )

        print(
            rejected_df[
                "rejection_reason"
            ].value_counts()
        )

    assert len(df) > 0


def test_mongodb_schema():
    df = load_mongodb(
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )

    expected_columns = [
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    ]

    assert list(df.columns) == expected_columns