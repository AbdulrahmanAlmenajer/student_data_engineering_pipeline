
from src.extract.csv_loader import load_csv
from src.extract.mongodb_loader import load_mongodb
from src.transform.merge import merge_student_data
from src.logger import logger
from src.extract.api_loader import extract_api
from src.pipeline import process_students

from src.load.csv_writer import save_csv
from src.load.sqlite_loader import load_to_sqlite


def main():

    logger.info(
        "Starting student data pipeline"
    )


    csv_df = load_csv(
        "data/raw/students.csv"
    )


    mongodb_df = load_mongodb(
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )
    api_df = extract_api(
        "http://localhost:8000/api/students"
    )

    csv_valid, csv_rejected = process_students(
        csv_df
    )


    mongo_valid, mongo_rejected = process_students(
        mongodb_df
    )
    api_valid, api_rejected = process_students(
        api_df
    )

    combined_valid, combined_rejected = merge_student_data(
        valid_dataframes=[
            csv_valid,
            mongo_valid,
        ],
        rejected_dataframes=[
            csv_rejected,
            mongo_rejected,
        ],
    )

    combined_valid = combined_valid.drop(
        columns=["rejection_reason"]
    )

    save_csv(
        combined_valid,
        "data/processed/students_valid.csv"
    )



    save_csv(
        combined_rejected,
        "data/processed/students_rejected.csv"
    )



    load_to_sqlite(
        combined_valid,
        "data/database/students.db"
    )



    print("\n===== COMBINED VALID DATA =====")
    print(combined_valid)

    print("\n===== COMBINED REJECTED DATA =====")
    print(combined_rejected)

    logger.info(
        "Pipeline completed successfully: "
        "%d valid, %d rejected",
        len(combined_valid),
        len(combined_rejected)
    )


if __name__ == "__main__":
    main()
