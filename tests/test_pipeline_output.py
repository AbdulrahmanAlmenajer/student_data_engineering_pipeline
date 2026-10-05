import sqlite3

import pandas as pd


def test_pipeline_sqlite_output():

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

    # Final number of unique valid students
    assert len(df) == 15

    # student_id must be unique
    assert df["student_id"].is_unique

    # Required columns
    expected_columns = [
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
        "_source",
    ]

    assert list(df.columns) == expected_columns

    # PostgreSQL has highest priority
    postgres_students = df[
        df["_source"] == "postgresql"
    ]

    assert len(postgres_students) == 10

    # PostgreSQL records must include these IDs
    expected_postgres_ids = {
        1001,
        1002,
        1003,
        1004,
        1005,
        1018,
        1019,
        1020,
        1021,
        1022,
    }

    assert set(
        postgres_students["student_id"]
    ) == expected_postgres_ids