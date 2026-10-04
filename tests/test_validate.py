import pandas as pd

from src.transform.validate import validate_students


def test_validate_students():
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002, 1003],
            "name": ["Ahmed", "Mohammed", "Ali"],
            "age": [22, 21, None],
            "gpa": [3.5, 3.8, 2.9],
            "attendance": [92, 88, 75],
            "city": ["Sanaa", "Taiz", "Ibb"],
        }
    )

    valid_df, rejected_df = validate_students(df)

    assert len(valid_df) == 2
    assert len(rejected_df) == 1

    assert rejected_df.iloc[0]["student_id"] == 1003

    assert (
        rejected_df.iloc[0]["rejection_reason"]
        == "invalid age"
    )


def test_invalid_gpa():
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", "Mohammed"],
            "age": [22, 21],
            "gpa": [3.5, 4.5],
            "attendance": [92, 88],
            "city": ["Sanaa", "Taiz"],
        }
    )

    valid_df, rejected_df = validate_students(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 1

    assert rejected_df.iloc[0]["student_id"] == 1002

    assert (
        rejected_df.iloc[0]["rejection_reason"]
        == "invalid gpa"
    )


def test_invalid_attendance():
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", "Mohammed"],
            "age": [22, 21],
            "gpa": [3.5, 3.8],
            "attendance": [92, 105],
            "city": ["Sanaa", "Taiz"],
        }
    )

    valid_df, rejected_df = validate_students(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 1

    assert rejected_df.iloc[0]["student_id"] == 1002

    assert (
        rejected_df.iloc[0]["rejection_reason"]
        == "invalid attendance"
    )

def test_multiple_rejection_reasons():
    df = pd.DataFrame(
        {
            "student_id": [None],
            "name": [""],
            "age": [None],
            "gpa": [5.0],
            "attendance": [120],
            "city": [""],
        }
    )

    valid_df, rejected_df = validate_students(df)

    assert len(valid_df) == 0
    assert len(rejected_df) == 1

    reason = rejected_df.iloc[0]["rejection_reason"]

    assert "missing student_id" in reason
    assert "missing name" in reason
    assert "invalid age" in reason
    assert "invalid gpa" in reason
    assert "invalid attendance" in reason
    assert "missing city" in reason

def test_duplicate_student_id():
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002, 1002],
            "name": ["Ahmed", "Mohammed", "Ali"],
            "age": [22, 21, 20],
            "gpa": [3.5, 3.8, 3.2],
            "attendance": [92, 88, 90],
            "city": ["Sanaa", "Taiz", "Ibb"],
        }
    )

    valid_df, rejected_df = validate_students(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 2

    assert all(
        rejected_df["student_id"] == 1002
    )

    assert all(
        rejected_df["rejection_reason"]
        == "duplicate student_id"
    )
from src.extract.csv_loader import load_csv
from src.transform.clean import clean_students


def test_validate_real_csv():
    df = load_csv("data/raw/students.csv")

    cleaned_df = clean_students(df)

    valid_df, rejected_df = validate_students(
        cleaned_df
    )

    assert len(valid_df) > 0
    assert len(rejected_df) > 0

    assert "rejection_reason" in rejected_df.columns

    assert (
        rejected_df["rejection_reason"]
        .ne("")
        .all()
    )


def test_missing_name_and_city():
    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", ""],
            "age": [22, 21],
            "gpa": [3.5, 3.8],
            "attendance": [92, 88],
            "city": ["Sanaa", ""],
        }
    )

    valid_df, rejected_df = validate_students(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 1

    assert rejected_df.iloc[0]["student_id"] == 1002

    reason = rejected_df.iloc[0]["rejection_reason"]

    assert "missing name" in reason
    assert "missing city" in reason