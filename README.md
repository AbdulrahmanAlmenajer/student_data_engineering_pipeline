# Student Data Pipeline

A Python-based data engineering pipeline for extracting, cleaning, validating, merging, and storing student data from multiple data sources.

## Project Overview

This project demonstrates a practical ETL/ELT-style data pipeline using Python.

The pipeline collects student data from multiple sources, applies common cleaning and validation rules, separates valid and rejected records, merges the processed data, and stores the final valid dataset in CSV and SQLite.

## Data Sources

The pipeline currently supports four data sources:

1. **CSV**
2. **MongoDB**
3. **REST API**
4. **PostgreSQL**

All sources are normalized to the same student schema before processing:

```text
student_id
name
age
gpa
attendance
city
```

## Pipeline Architecture

```text
                    ┌─────────────┐
                    │     CSV     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   MongoDB   │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │     API     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ PostgreSQL  │
                    └──────┬──────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │ Clean & Validate │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Merge Data       │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Valid / Rejected │
                 └────────┬─────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
       students_valid.csv      students_rejected.csv
             │
             ▼
        SQLite Database
```

## Project Structure

```text
student_data_pipeline/
│
├── data/
│   ├── raw/
│   │   └── students.csv
│   │
│   ├── processed/
│   │   ├── students_valid.csv
│   │   └── students_rejected.csv
│   │
│   └── database/
│       └── students.db
│
├── scripts/
│   └── setup_postgres.py
│
├── src/
│   ├── extract/
│   │   ├── csv_loader.py
│   │   ├── mongodb_loader.py
│   │   ├── api_loader.py
│   │   └── postgres_loader.py
│   │
│   ├── transform/
│   │   ├── clean.py
│   │   ├── validate.py
│   │   └── merge.py
│   │
│   ├── load/
│   │   ├── csv_writer.py
│   │   └── sqlite_loader.py
│   │
│   ├── pipeline.py
│   └── logger.py
│
├── tests/
│   ├── test_clean.py
│   ├── test_validate.py
│   ├── test_merge.py
│   ├── test_csv_loader.py
│   ├── test_mongodb_loader.py
│   ├── test_api_loader.py
│   └── test_postgres_loader.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Technologies

- Python 3.14
- Pandas
- Pytest
- MongoDB
- PostgreSQL
- SQLite
- REST API
- Git / GitHub

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/student_data_pipeline.git
cd student_data_pipeline
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

## PostgreSQL Setup

The PostgreSQL database can be created using the Python setup script:

```powershell
python scripts/setup_postgres.py
```

The script creates:

```text
Database:
students_db

Table:
students
```

Table schema:

```text
student_id
name
age
gpa
attendance
city
```

## MongoDB

The MongoDB extractor connects to the configured MongoDB database and collection and converts the returned documents into a Pandas DataFrame.

The MongoDB connection settings are configured in `main.py`.

## API

The pipeline includes a REST API extractor.

Current development endpoint:

```text
http://localhost:8000/api/students
```

The API returns student records using the common project schema.

## Data Processing

Each source passes through the same processing pipeline:

```text
Extract
   ↓
Clean
   ↓
Validate
   ↓
Valid / Rejected
```

Invalid records are not silently discarded.

They are stored separately with a `rejection_reason` column explaining why the record was rejected.

Examples:

```text
invalid age
invalid gpa
invalid attendance
missing name
missing city
missing student_id
duplicate student_id
```

## Output

The pipeline generates:

### Valid records

```text
data/processed/students_valid.csv
```

### Rejected records

```text
data/processed/students_rejected.csv
```

### SQLite database

```text
data/database/students.db
```

## Running the Pipeline

Run:

```powershell
python main.py
```

The pipeline logs each major operation, including:

- Source extraction
- Number of rows loaded
- Data processing
- Validation results
- Merge results
- Output generation
- SQLite loading

## Testing

Run all tests:

```powershell
python -m pytest tests -v
```

Run a specific source test:

```powershell
python -m pytest tests/test_postgres_loader.py -v -s
```

## Current PostgreSQL Test

The PostgreSQL extractor has been successfully tested:

```text
1 passed
```

The extractor successfully loaded:

```text
10 rows
6 columns
```

from PostgreSQL.

## Logging

The project uses a centralized logger:

```python
from src.logger import logger
```

Log messages include timestamps and log levels.

Example:

```text
2026-10-05 17:28:20 | INFO | PostgreSQL loaded successfully: 10 rows, 6 columns
```

## Current Pipeline Status

| Source | Status |
|---|---|
| CSV | ✅ Completed |
| MongoDB | ✅ Completed |
| REST API | ✅ Completed |
| PostgreSQL | ✅ Completed |
| Cleaning | ✅ Completed |
| Validation | ✅ Completed |
| Merge | ✅ Implemented |
| CSV Output | ✅ Implemented |
| SQLite Output | ✅ Implemented |
| Automated Tests | ✅ Implemented |

## Future Improvements

Planned improvements include:

- Improving PostgreSQL connectivity using SQLAlchemy
- Moving database credentials to environment variables
- Reviewing cross-source duplicate handling
- Reviewing source priority for duplicate student IDs
- Investigating row-count differences after merging sources
- Adding more data sources
- Improving pipeline configuration
- Adding CI/CD with GitHub Actions

## Author

**Abdulrhman Hussin**

Student Data Engineering Project