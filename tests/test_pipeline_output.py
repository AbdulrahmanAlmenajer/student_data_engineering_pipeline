
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


    assert len(df) == 7


    expected_columns = [
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    ]

    assert list(df.columns) == expected_columns


    assert df["student_id"].notna().all()


    assert df["student_id"].is_unique


    assert df["age"].between(15, 100).all()
    assert df["gpa"].between(0, 4).all()
    assert df["attendance"].between(0, 100).all()
