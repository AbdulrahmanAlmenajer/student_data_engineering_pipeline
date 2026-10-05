import pandas as pd
import pytest

from src.extract.api_loader import extract_api


API_URL = "http://localhost:8000/api/students"


def test_extract_api():
    df = extract_api(API_URL)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5

    assert "student_id" in df.columns
    assert "name" in df.columns
    assert "age" in df.columns
    assert "gpa" in df.columns
    assert "attendance" in df.columns
    assert "city" in df.columns


def test_extract_api_data():
    df = extract_api(API_URL)

    assert df.loc[0, "student_id"] == "1001"
    assert df.loc[0, "name"] == "Ahmed"
    assert df.loc[0, "age"] == 22
    assert df.loc[0, "gpa"] == 3.8
    assert df.loc[0, "attendance"] == 95
    assert df.loc[0, "city"] == "Sanaa"


def test_extract_api_invalid_url():
    with pytest.raises(Exception):
        extract_api("http://localhost:8000/api/invalid")