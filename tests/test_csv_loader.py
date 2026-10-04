from pathlib import Path

from src.extract.csv_loader import load_csv


def test_load_csv():
    file_path = Path("data/raw/students.csv")

    df = load_csv(file_path)

    required_columns = {
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    }

    assert not df.empty
    assert set(required_columns).issubset(df.columns)