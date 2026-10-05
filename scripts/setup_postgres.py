import os

import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv


load_dotenv()


# ============================================
# PostgreSQL configuration
# ============================================

HOST = os.getenv("POSTGRES_HOST", "localhost")
PORT = int(os.getenv("POSTGRES_PORT", "5432"))
USER = os.getenv("POSTGRES_USER", "postgres")
PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE = os.getenv("POSTGRES_DATABASE", "students_db")

TABLE = "students"


# ============================================
# Student data
# ============================================

STUDENTS = [
    (1001, "Ahmed", 22, 3.90, 95, "Sanaa"),
    (1002, "Mohammed", 21, 3.70, 90, "Taiz"),
    (1003, "Khaled", 23, 3.60, 88, "Ibb"),
    (1004, "Ali", 20, 3.50, 92, "Sanaa"),
    (1005, "Salma", 19, 3.80, 96, "Dhamar"),
    (1018, "Hassan", 24, 3.40, 85, "Taiz"),
    (1019, "Fatima", 21, 3.90, 94, "Ibb"),
    (1020, "Omar", 22, 3.20, 80, "Sanaa"),
    (1021, "Nour", 20, 3.60, 91, "Dhamar"),
    (1022, "Yousef", 23, 3.30, 87, "Sanaa"),
]


# ============================================
# Create database
# ============================================

def create_database():
    connection = None

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database="postgres",
        )

        connection.autocommit = True

        cursor = connection.cursor()

        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DATABASE,),
        )

        exists = cursor.fetchone()

        if exists:
            print(f"Database already exists: {DATABASE}")
        else:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DATABASE)
                )
            )

            print(f"Database created: {DATABASE}")

        cursor.close()

    finally:
        if connection is not None:
            connection.close()


# ============================================
# Create table and insert data
# ============================================

def create_table_and_insert_data():
    connection = None

    try:
        connection = psycopg2.connect(
            host=HOST,
            port=PORT,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
        )

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY,
                name VARCHAR(100),
                age INTEGER,
                gpa NUMERIC(3, 2),
                attendance NUMERIC(5, 2),
                city VARCHAR(100)
            )
            """
        )

        insert_query = """
            INSERT INTO students (
                student_id,
                name,
                age,
                gpa,
                attendance,
                city
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (student_id)
            DO UPDATE SET
                name = EXCLUDED.name,
                age = EXCLUDED.age,
                gpa = EXCLUDED.gpa,
                attendance = EXCLUDED.attendance,
                city = EXCLUDED.city
        """

        cursor.executemany(
            insert_query,
            STUDENTS,
        )

        connection.commit()

        print(f"Table created: {TABLE}")
        print(f"Students inserted/updated: {len(STUDENTS)}")

        cursor.execute(
            """
            SELECT
                student_id,
                name,
                age,
                gpa,
                attendance,
                city
            FROM students
            ORDER BY student_id
            """
        )

        rows = cursor.fetchall()

        print("\n===== PostgreSQL Students =====")

        for row in rows:
            print(row)

        cursor.close()

    except psycopg2.Error as e:
        if connection is not None:
            connection.rollback()

        print(f"PostgreSQL error: {e}")
        raise

    finally:
        if connection is not None:
            connection.close()


# ============================================
# Main
# ============================================

def main():
    print("Starting PostgreSQL setup...\n")

    create_database()

    create_table_and_insert_data()

    print("\nPostgreSQL setup completed successfully.")


if __name__ == "__main__":
    main()