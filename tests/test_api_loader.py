import pandas as pd
import pytest

from src.extract.api_loader import extract_api


API_URL = "http://localhost:8000/api/students"

EXPECTED_COLUMNS = [
    "student_id",
    "name",
    "age",
    "gpa",
    "attendance",
    "city",
]


def test_extract_api_returns_dataframe():
    """Test that extract_api returns a DataFrame."""

    df = extract_api(API_URL)

    assert isinstance(df, pd.DataFrame)


def test_extract_api_row_count():
    """Test that mock API returns expected
    number of records."""

    df = extract_api(API_URL)

    assert len(df) == 5


def test_extract_api_columns():
    """Test that all required columns are
    present in the result."""

    df = extract_api(API_URL)

    for col in EXPECTED_COLUMNS:
        assert col in df.columns, (
            f"Missing column: {col}"
        )


def test_extract_api_first_row():
    """Test the values of the first record
    from the mock API."""

    df = extract_api(API_URL)

    assert df.loc[0, "student_id"] == "1001"
    assert df.loc[0, "name"] == "Ahmed"
    assert df.loc[0, "age"] == 22
    assert df.loc[0, "gpa"] == 3.8
    assert df.loc[0, "attendance"] == 95
    assert df.loc[0, "city"] == "Sanaa"


def test_extract_api_handles_null_values():
    """Test that rows with None values
    (gpa, attendance) are included."""

    df = extract_api(API_URL)

    # Row 4 (index 4) has None for gpa and attendance
    assert pd.isna(df.loc[4, "gpa"])
    assert pd.isna(df.loc[4, "attendance"])


def test_extract_api_invalid_url():
    """Test that an unknown URL raises
    an exception (not silently ignored)."""

    with pytest.raises(Exception):
        extract_api(
            "http://localhost:8000/api/invalid"
        )