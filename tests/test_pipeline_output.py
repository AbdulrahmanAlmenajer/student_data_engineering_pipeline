import sqlite3

import pandas as pd


EXPECTED_COLUMNS = [
    "student_id",
    "name",
    "age",
    "gpa",
    "attendance",
    "city",
    "_source",
]


def test_pipeline_sqlite_output():
    """Test that the SQLite database was
    created and populated by the pipeline."""

    connection = sqlite3.connect(
        "data/database/students.db"
    )

    try:
        df = pd.read_sql_query(
            "SELECT * FROM students",
            connection,
        )

    finally:
        connection.close()

    # Database must have at least one record
    assert len(df) > 0

    # student_id must be unique
    assert df["student_id"].is_unique

    # All required columns must exist
    for col in EXPECTED_COLUMNS:
        assert col in df.columns, (
            f"Missing column: {col}"
        )

    # Every record must have a source
    assert df["_source"].notna().all()
    assert df["_source"].ne("").all()


def test_pipeline_sqlite_valid_ranges():
    """Test that all values in the SQLite
    database are within valid ranges after
    cleaning and validation."""

    connection = sqlite3.connect(
        "data/database/students.db"
    )

    try:
        df = pd.read_sql_query(
            "SELECT * FROM students",
            connection,
        )

    finally:
        connection.close()

    # Age must be in valid range
    assert (df["age"] >= 15).all()
    assert (df["age"] <= 100).all()

    # GPA must be in valid range
    assert (df["gpa"] >= 0).all()
    assert (df["gpa"] <= 4).all()

    # Attendance must be in valid range
    assert (df["attendance"] >= 0).all()
    assert (df["attendance"] <= 100).all()

    # No missing names or cities
    assert df["name"].notna().all()
    assert df["city"].notna().all()