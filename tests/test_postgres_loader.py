import pandas as pd

from src.extract.postgres_loader import load_postgres


def test_load_postgres():

    df = load_postgres(
        host="localhost",
        port=5432,
        database="students_db",
        user="postgres",
        password="postgres",
        table="students",
    )

    assert isinstance(df, pd.DataFrame)

    assert "student_id" in df.columns
    assert "name" in df.columns
    assert "age" in df.columns
    assert "gpa" in df.columns
    assert "attendance" in df.columns
    assert "city" in df.columns