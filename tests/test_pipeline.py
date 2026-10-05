import pandas as pd

from src.pipeline import process_students


def test_process_students():
    df = pd.DataFrame({
        "student_id": [1001, 1002, 1003],
        "name": ["Ahmed", "Sara", "Ali"],
        "age": [22, 21, 150],
        "gpa": [3.5, 3.8, 3.0],
        "attendance": [92, 88, 90],
        "city": ["Sanaa", "Taiz", "Ibb"],
    })

    valid_df, rejected_df = process_students(df)

    assert len(valid_df) == 2
    assert len(rejected_df) == 1

    assert valid_df["student_id"].tolist() == [
        1001,
        1002,
    ]

    assert rejected_df["student_id"].tolist() == [
        1003,
    ]

    assert rejected_df[
        "rejection_reason"
    ].iloc[0] == "invalid age"