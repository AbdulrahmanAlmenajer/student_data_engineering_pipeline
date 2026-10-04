from pathlib import Path

from src.extract.csv_loader import load_csv


def test_load_csv():
    file_path = Path("data/raw/students.csv")

    df = load_csv(file_path)

    assert not df.empty
    assert len(df) == 5
    assert "student_id" in df.columns
    assert "name" in df.columns
    assert "gpa" in df.columns