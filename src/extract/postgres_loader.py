import pandas as pd
import psycopg2

from src.logger import logger


def load_postgres(
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
    table: str,
) -> pd.DataFrame:
    """
    Load student data from PostgreSQL.
    """

    logger.info(
        "Starting PostgreSQL extraction: %s.%s",
        database,
        table,
    )

    connection = None

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

        query = f"""
            SELECT
                student_id,
                name,
                age,
                gpa,
                attendance,
                city
            FROM {table}
        """

        df = pd.read_sql_query(
            query,
            connection,
        )

        logger.info(
            "PostgreSQL loaded successfully: %d rows, %d columns",
            len(df),
            len(df.columns),
        )

        return df

    except psycopg2.Error as e:
        logger.error(
            "PostgreSQL error: %s",
            e,
        )
        raise

    except Exception as e:
        logger.error(
            "Error extracting PostgreSQL: %s",
            e,
        )
        raise

    finally:
        if connection is not None:
            connection.close()
            logger.info(
                "PostgreSQL connection closed"
            )