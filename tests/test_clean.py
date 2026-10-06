import pandas as pd
import numpy as np

from src.transform.clean import clean_students


def test_clean_column_names():
    """Test that column names are standardized."""

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


def test_clean_text_strip_and_capitalize():
    """Test that text columns are stripped
    and title-cased."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["  ahmed  ", "  SARA  "],
            "age": [22, 20],
            "gpa": [3.5, 3.9],
            "attendance": [92, 97],
            "city": ["  sanaa  ", "  TAIZ  "],
        }
    )

    cleaned = clean_students(df)

    assert cleaned.loc[0, "name"] == "Ahmed"
    assert cleaned.loc[1, "name"] == "Sara"
    assert cleaned.loc[0, "city"] == "Sanaa"
    assert cleaned.loc[1, "city"] == "Taiz"


def test_clean_numeric_conversion():
    """Test that invalid numeric values
    are coerced to NaN then filled."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", "Hassan"],
            "age": ["22", "abc"],
            "gpa": [3.5, 3.7],
            "attendance": [92, 91],
            "city": ["Sanaa", "Taiz"],
        }
    )

    cleaned = clean_students(df)

    # "abc" should be coerced to NaN and
    # then filled with median (= 22)
    assert pd.notna(cleaned.loc[1, "age"])
    assert cleaned.loc[0, "age"] == 22


def test_clean_removes_full_duplicates():
    """Test that full duplicate rows
    are removed."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1001],
            "name": ["Ahmed", "Ahmed"],
            "age": [22, 22],
            "gpa": [3.5, 3.5],
            "attendance": [92, 92],
            "city": ["Sanaa", "Sanaa"],
        }
    )

    cleaned = clean_students(df)

    assert len(cleaned) == 1


def test_clean_fill_missing_age_with_median():
    """Test that missing age is filled
    with median."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002, 1003],
            "name": ["Ahmed", "Sara", "Ali"],
            "age": [20, None, 24],
            "gpa": [3.5, 3.9, 3.0],
            "attendance": [92, 97, 80],
            "city": ["Sanaa", "Taiz", "Ibb"],
        }
    )

    cleaned = clean_students(df)

    # Median of [20, 24] = 22
    assert cleaned.loc[1, "age"] == 22
    assert cleaned["age"].isna().sum() == 0


def test_clean_fill_missing_gpa_with_mean():
    """Test that missing GPA is filled
    with mean."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002, 1003],
            "name": ["Ahmed", "Sara", "Ali"],
            "age": [22, 20, 21],
            "gpa": [3.0, None, 4.0],
            "attendance": [92, 97, 80],
            "city": ["Sanaa", "Taiz", "Ibb"],
        }
    )

    cleaned = clean_students(df)

    # Mean of [3.0, 4.0] = 3.5
    assert cleaned.loc[1, "gpa"] == 3.5
    assert cleaned["gpa"].isna().sum() == 0


def test_clean_fill_missing_attendance_with_median():
    """Test that missing attendance is filled
    with median."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002, 1003],
            "name": ["Ahmed", "Sara", "Ali"],
            "age": [22, 20, 21],
            "gpa": [3.5, 3.9, 3.0],
            "attendance": [80, None, 90],
            "city": ["Sanaa", "Taiz", "Ibb"],
        }
    )

    cleaned = clean_students(df)

    # Median of [80, 90] = 85
    assert cleaned.loc[1, "attendance"] == 85.0
    assert (
        cleaned["attendance"].isna().sum() == 0
    )


def test_clean_fill_missing_city_with_mode():
    """Test that missing city is filled
    with mode."""

    df = pd.DataFrame(
        {
            "student_id": [
                1001, 1002, 1003, 1004
            ],
            "name": [
                "Ahmed", "Sara", "Ali", "Omar"
            ],
            "age": [22, 20, 21, 23],
            "gpa": [3.5, 3.9, 3.0, 3.2],
            "attendance": [92, 97, 80, 88],
            "city": ["Sanaa", "Sanaa", "", ""],
        }
    )

    cleaned = clean_students(df)

    # Mode = "Sanaa"
    assert cleaned.loc[2, "city"] == "Sanaa"
    assert cleaned.loc[3, "city"] == "Sanaa"


def test_clean_cap_outliers():
    """Test that extreme outliers
    are capped."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002, 1003],
            "name": ["Ahmed", "Sara", "Ali"],
            "age": [22, 20, 200],
            "gpa": [3.5, 3.9, 10.0],
            "attendance": [92, 97, 200],
            "city": ["Sanaa", "Taiz", "Ibb"],
        }
    )

    cleaned = clean_students(df)

    # Age 200 should be capped
    assert cleaned.loc[2, "age"] <= 100

    # GPA 10.0 should be capped at 4.0
    assert cleaned.loc[2, "gpa"] <= 4.0

    # Attendance 200 should be capped at 100
    assert cleaned.loc[2, "attendance"] <= 100


def test_clean_rounds_numeric_columns():
    """Test that numeric columns are
    properly rounded."""

    df = pd.DataFrame(
        {
            "student_id": [1001],
            "name": ["Ahmed"],
            "age": [22],
            "gpa": [3.14159],
            "attendance": [92.567],
            "city": ["Sanaa"],
        }
    )

    cleaned = clean_students(df)

    # GPA should be rounded to 2 decimal places
    assert cleaned.loc[0, "gpa"] == 3.14

    # Attendance should be rounded to 1 decimal
    assert cleaned.loc[0, "attendance"] == 92.6


def test_clean_preserves_valid_data():
    """Test that valid data is preserved
    unchanged."""

    df = pd.DataFrame(
        {
            "student_id": [1001, 1002],
            "name": ["Ahmed", "Sara"],
            "age": [22, 20],
            "gpa": [3.5, 3.9],
            "attendance": [92, 97],
            "city": ["Sanaa", "Taiz"],
        }
    )

    cleaned = clean_students(df)

    assert len(cleaned) == 2
    assert cleaned.loc[0, "name"] == "Ahmed"
    assert cleaned.loc[0, "gpa"] == 3.5
    assert cleaned.loc[0, "attendance"] == 92


def test_clean_empty_dataframe():
    """Test that cleaning handles
    empty DataFrames."""

    df = pd.DataFrame(
        columns=[
            "student_id",
            "name",
            "age",
            "gpa",
            "attendance",
            "city",
        ]
    )

    cleaned = clean_students(df)

    assert len(cleaned) == 0
    assert list(cleaned.columns) == [
        "student_id",
        "name",
        "age",
        "gpa",
        "attendance",
        "city",
    ]


def test_clean_real_csv():
    """Integration test with real CSV data."""

    from src.extract.csv_loader import load_csv

    df = load_csv("data/raw/students.csv")
    cleaned = clean_students(df)

    # Should have fewer or equal rows
    # (duplicates removed)
    assert len(cleaned) <= len(df)

    # No missing values in numeric columns
    # after cleaning
    assert cleaned["age"].isna().sum() == 0
    assert cleaned["gpa"].isna().sum() == 0
    assert (
        cleaned["attendance"].isna().sum() == 0
    )