import sqlite3

import pandas as pd

from src.load.sqlite_loader import load_to_sqlite


def test_load_to_sqlite(tmp_path):
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", "Sara"],
            "gpa": [3.5, 3.9],
        }
    )

    db_path = (
        tmp_path / "students.db"
    )

    load_to_sqlite(
        df,
        db_path
    )

    assert db_path.exists()

    connection = sqlite3.connect(
        db_path
    )

    try:
        result = pd.read_sql_query(
            "SELECT * FROM students",
            connection
        )

    finally:
        connection.close()

    assert len(result) == 2

    assert list(result.columns) == [
        "student_id",
        "name",
        "gpa",
    ]

    assert result.loc[0, "name"] == "Ahmed"
    assert result.loc[1, "gpa"] == 3.9