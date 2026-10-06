import pandas as pd

from src.transform.merge import merge_student_data


def test_merge_student_data():
    """Test that valid and rejected frames
    from multiple sources are merged correctly."""

    valid_1 = pd.DataFrame({
        "student_id": [1001, 1002],
        "name": ["Ahmed", "Mohammed"],
    })

    valid_2 = pd.DataFrame({
        "student_id": [1007],
        "name": ["Ahmed Ali"],
    })

    rejected_1 = pd.DataFrame({
        "student_id": [1003],
        "name": ["Ali"],
        "rejection_reason": ["invalid age"],
    })

    rejected_2 = pd.DataFrame({
        "student_id": [1008],
        "name": ["Fatima"],
        "rejection_reason": ["invalid gpa"],
    })

    combined_valid, combined_rejected = merge_student_data(
        valid_dataframes=[
            ("csv", valid_1),
            ("mongodb", valid_2),
        ],
        rejected_dataframes=[
            ("csv", rejected_1),
            ("mongodb", rejected_2),
        ],
    )

    assert len(combined_valid) == 3
    assert len(combined_rejected) == 2

    assert combined_valid[
        "student_id"
    ].tolist() == [1001, 1002, 1007]

    assert combined_rejected[
        "student_id"
    ].tolist() == [1003, 1008]


def test_merge_student_data_source_priority():
    """Test that the highest-priority source
    wins when duplicate student_ids exist."""

    csv_df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed CSV"],
    })

    api_df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed API"],
    })

    mongodb_df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed MongoDB"],
    })

    postgres_df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed PostgreSQL"],
    })

    combined_valid, combined_rejected = merge_student_data(
        valid_dataframes=[
            ("csv", csv_df),
            ("api", api_df),
            ("mongodb", mongodb_df),
            ("postgresql", postgres_df),
        ],
        rejected_dataframes=[],
    )

    assert len(combined_valid) == 1
    assert len(combined_rejected) == 0
    assert (
        combined_valid.loc[0, "name"]
        == "Ahmed PostgreSQL"
    )


def test_merge_adds_source_column_to_valid():
    """Test that _source column is added
    to valid DataFrame."""

    df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed"],
    })

    combined_valid, _ = merge_student_data(
        valid_dataframes=[("csv", df)],
        rejected_dataframes=[],
    )

    assert "_source" in combined_valid.columns
    assert combined_valid.loc[0, "_source"] == "csv"


def test_merge_adds_source_column_to_rejected():
    """Test that _source column is added
    to rejected DataFrame."""

    df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed"],
        "rejection_reason": ["invalid age"],
    })

    _, combined_rejected = merge_student_data(
        valid_dataframes=[],
        rejected_dataframes=[("csv", df)],
    )

    assert "_source" in combined_rejected.columns
    assert (
        combined_rejected.loc[0, "_source"] == "csv"
    )


def test_merge_skips_empty_dataframes():
    """Test that empty DataFrames are
    handled gracefully."""

    valid_df = pd.DataFrame({
        "student_id": [1001],
        "name": ["Ahmed"],
    })

    empty_df = pd.DataFrame(
        columns=["student_id", "name"]
    )

    combined_valid, combined_rejected = merge_student_data(
        valid_dataframes=[
            ("csv", valid_df),
            ("mongodb", empty_df),
        ],
        rejected_dataframes=[],
    )

    assert len(combined_valid) == 1
    assert len(combined_rejected) == 0