import pandas as pd

from src.load.csv_writer import save_csv


def test_save_csv(tmp_path):
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", "Sara"],
            "gpa": [3.5, 3.9],
        }
    )

    output_file = tmp_path / "students.csv"

    save_csv(
        df,
        output_file
    )

    assert output_file.exists()

    saved_df = pd.read_csv(
        output_file
    )

    assert len(saved_df) == 2
    assert list(saved_df.columns) == [
        "student_id",
        "name",
        "gpa",
    ]

    assert saved_df.loc[0, "name"] == "Ahmed"
    assert saved_df.loc[1, "gpa"] == 3.9