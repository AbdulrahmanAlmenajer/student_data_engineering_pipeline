import pandas as pd

from src.transform.clean import clean_students


def test_clean_students():

    df = pd.DataFrame(
        {
            "Student_ID": [1001, 1002],
            " Name ": [" Ahmed ", " Sara "],
            "Age": ["22", "20"],
            "GPA": ["3.5", "3.9"],
            "Attendance": ["92", "97"],
            "City": [" Sanaa ", "Sanaa"],
        }
    )

    cleaned = clean_students(df)

    assert list(cleaned.columns) == [
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    ]

    assert cleaned.loc[0, "name"] == "Ahmed"
    assert cleaned.loc[0, "city"] == "Sanaa"
    assert cleaned.loc[0, "age"] == 22
    assert cleaned.loc[0, "gpa"] == 3.5