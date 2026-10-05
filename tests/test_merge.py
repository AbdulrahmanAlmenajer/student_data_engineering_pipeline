
import pandas as pd

from src.transform.merge import merge_student_data


def test_merge_student_data():

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
            valid_1,
            valid_2,
        ],
        rejected_dataframes=[
            rejected_1,
            rejected_2,
        ],
    )

    assert len(combined_valid) == 3
    assert len(combined_rejected) == 2

    assert combined_valid[
        "student_id"
    ].tolist() == [
        1001,
        1002,
        1007,
    ]

    assert combined_rejected[
        "student_id"
    ].tolist() == [
        1003,
        1008,
    ]
