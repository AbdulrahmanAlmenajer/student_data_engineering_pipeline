import pandas as pd

from src.pipeline import process_students


def test_process_students():
    """Test the full pipeline: clean + validate.

    With the enhanced cleaner, outlier values
    like age=150 are capped (not rejected).
    Only truly invalid records (missing student_id,
    missing name, etc.) get rejected.
    """

    df = pd.DataFrame({
        "student_id": [1001, 1002, 1003],
        "name": ["Ahmed", "Sara", "Ali"],
        "age": [22, 21, 150],
        "gpa": [3.5, 3.8, 3.0],
        "attendance": [92, 88, 90],
        "city": ["Sanaa", "Taiz", "Ibb"],
    })

    valid_df, rejected_df = process_students(df)

    # Age=150 is now capped by the cleaner,
    # so all 3 records should be valid
    assert len(valid_df) == 3
    assert len(rejected_df) == 0

    assert 1001 in valid_df["student_id"].tolist()
    assert 1002 in valid_df["student_id"].tolist()
    assert 1003 in valid_df["student_id"].tolist()


def test_process_students_with_rejection():
    """Test that records with missing required
    fields are still rejected."""

    df = pd.DataFrame({
        "student_id": [1001, None],
        "name": ["Ahmed", ""],
        "age": [22, 21],
        "gpa": [3.5, 3.8],
        "attendance": [92, 88],
        "city": ["Sanaa", "Taiz"],
    })

    valid_df, rejected_df = process_students(df)

    assert len(valid_df) == 1
    assert len(rejected_df) == 1

    reason = rejected_df.iloc[0][
        "rejection_reason"
    ]
    assert "missing student_id" in reason
    assert "missing name" in reason