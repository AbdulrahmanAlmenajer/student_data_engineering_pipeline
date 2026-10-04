from src.load.sqlite_loader import load_to_sqlite
from src.load.csv_writer import save_csv
from src.extract.csv_loader import load_csv
from src.logger import logger
from src.transform.clean import clean_students
from src.transform.validate import validate_students


def main():
    logger.info("Starting student data pipeline")

    # Extract
    df = load_csv(
        "data/raw/students.csv"
    )

    # Clean
    cleaned_df = clean_students(df)

    # Validate
    valid_df, rejected_df = validate_students(
        cleaned_df
    )
    save_csv(
        valid_df,
        "data/processed/students_valid.csv"
    )

    save_csv(
        rejected_df,
        "data/processed/students_rejected.csv"
    )
    load_to_sqlite(
        valid_df,
        "data/database/students.db"
    )

    print("\n===== VALID DATA =====")
    print(valid_df)

    print("\n===== REJECTED DATA =====")
    print(rejected_df)

    logger.info(
        "Pipeline completed successfully"
    )


if __name__ == "__main__":
    main()