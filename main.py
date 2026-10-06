import os

from dotenv import load_dotenv

from src.extract.csv_loader import load_csv
from src.extract.mongodb_loader import load_mongodb
from src.extract.api_loader import extract_api
from src.extract.postgres_loader import load_postgres

from src.transform.merge import merge_student_data
from src.logger import logger
from src.pipeline import process_students

from src.load.csv_writer import save_csv
from src.load.sqlite_loader import load_to_sqlite


load_dotenv()


def _safe_load(source_name: str, loader_fn, *args, **kwargs):
    """
    Call a loader function and return an empty
    list if the source is unavailable.

    This allows the pipeline to continue even
    when one data source is offline.

    Returns:
        DataFrame from the loader, or None on failure.
    """

    try:
        return loader_fn(*args, **kwargs)

    except Exception as e:
        logger.warning(
            "Source '%s' failed, skipping: %s",
            source_name,
            e,
        )
        return None


def main():

    logger.info("Starting student data pipeline")

    # ==========================================
    # Extract
    # ==========================================

    csv_df = load_csv("data/raw/students.csv")

    mongodb_df = _safe_load(
        "mongodb",
        load_mongodb,
        "mongodb://localhost:27017/",
        "Universty_Genius",
        "student",
    )

    api_df = _safe_load(
        "api",
        extract_api,
        "http://localhost:8000/api/students",
    )

    postgres_df = _safe_load(
        "postgresql",
        load_postgres,
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv(
            "POSTGRES_DATABASE", "students_db"
        ),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD"),
        table="students",
    )

    # ==========================================
    # Process each source
    # ==========================================

    csv_valid, csv_rejected = process_students(
        csv_df
    )

    valid_dfs = [("csv", csv_valid)]
    rejected_dfs = [("csv", csv_rejected)]

    if mongodb_df is not None:
        mongo_valid, mongo_rejected = process_students(
            mongodb_df
        )
        valid_dfs.append(("mongodb", mongo_valid))
        rejected_dfs.append(("mongodb", mongo_rejected))

    if api_df is not None:
        api_valid, api_rejected = process_students(
            api_df
        )
        valid_dfs.append(("api", api_valid))
        rejected_dfs.append(("api", api_rejected))

    if postgres_df is not None:
        postgres_valid, postgres_rejected = (
            process_students(postgres_df)
        )
        valid_dfs.append(("postgresql", postgres_valid))
        rejected_dfs.append(
            ("postgresql", postgres_rejected)
        )

    # ==========================================
    # Merge all sources
    # ==========================================

    combined_valid, combined_rejected = (
        merge_student_data(
            valid_dataframes=valid_dfs,
            rejected_dataframes=rejected_dfs,
        )
    )

    # Drop rejection_reason from the valid output
    combined_valid = combined_valid.drop(
        columns=["rejection_reason"]
    )

    # ==========================================
    # Save outputs
    # ==========================================

    save_csv(
        combined_valid,
        "data/processed/students_valid.csv",
    )

    save_csv(
        combined_rejected,
        "data/processed/students_rejected.csv",
    )

    load_to_sqlite(
        combined_valid,
        "data/database/students.db",
    )

    # ==========================================
    # Summary
    # ==========================================

    print("\n===== COMBINED VALID DATA =====")
    print(combined_valid)

    print("\n===== COMBINED REJECTED DATA =====")
    print(combined_rejected)

    logger.info(
        "Pipeline completed successfully: "
        "%d valid, %d rejected",
        len(combined_valid),
        len(combined_rejected),
    )


if __name__ == "__main__":
    main()