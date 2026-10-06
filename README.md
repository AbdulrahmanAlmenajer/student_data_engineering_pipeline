# Student Data Pipeline

A Python-based data engineering pipeline for extracting, cleaning, validating, merging, and storing student data from multiple data sources.

> **Fault-tolerant**: The pipeline continues running even if MongoDB, API, or PostgreSQL are offline. Only the CSV source is required.

## Project Overview

This project demonstrates a practical ETL/ELT-style data pipeline using Python.

The pipeline collects student data from multiple sources, applies comprehensive data cleaning (including statistical imputation and outlier detection), validates records, separates valid and rejected data, merges the processed data, and stores the final valid dataset in CSV and SQLite.

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
              ┌────────────────────────┐
              │   Comprehensive Clean  │
              │  (9-Step Data Cleaning)│
              └───────────┬────────────┘
                          │
                 ┌────────▼─────────┐
                 │     Validate     │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │   Merge Data     │
                 └────────┬─────────┘
                          │
                 ┌────────▼─────────┐
                 │ Valid / Rejected  │
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
│   ├── test_csv_writer.py
│   ├── test_mongodb_loader.py
│   ├── test_api_loader.py
│   ├── test_postgres_loader.py
│   ├── test_pipeline.py
│   ├── test_pipeline_output.py
│   ├── test_source_merge.py
│   └── test_sqlite_loader.py
│
├── main.py
├── requirements.txt
└── README.md
```

## Technologies

- Python 3.14
- Pandas
- NumPy
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
Clean (9 Steps)
   ↓
Validate
   ↓
Valid / Rejected
```

### Data Cleaning (9 Steps)

The cleaning module (`src/transform/clean.py`) applies a comprehensive 9-step cleaning process:

| Step | Operation | Details |
|------|-----------|---------|
| 1 | **Standardize Column Names** | Strip whitespace, convert to lowercase |
| 2 | **Remove Full Duplicate Rows** | Drop rows that are completely identical |
| 3 | **Clean Text Columns** | Strip whitespace, remove special characters, apply Title Case |
| 4 | **Convert Numeric Columns** | Coerce invalid values (e.g., `"abc"`, `"twenty"`) to `NaN` |
| 5 | **Fill Missing Numeric Values** | `age` → Median, `gpa` → Mean, `attendance` → Median |
| 6 | **Fill Missing Text Values** | `city` → Mode (most frequent value) |
| 7 | **Cap Outliers (IQR Method)** | Detect and cap outliers using IQR + domain bounds |
| 8 | **Round Numeric Columns** | `age` → integer, `gpa` → 2 decimals, `attendance` → 1 decimal |
| 9 | **Generate Cleaning Report** | Log descriptive statistics (Mean, Median, Std, Q1, Q3, Min, Max) |

### Statistical Methods Used

**Median** for `age` and `attendance`:

- Robust to outliers
- Best choice when data distribution may be skewed

**Mean** for `gpa`:

- Sensitive to the full distribution
- Appropriate when values follow a normal distribution (0–4 scale)

**Mode** for `city`:

- Categorical data cannot use Mean or Median
- The most frequent value is the logical default

**IQR Method** for outlier detection:

```text
Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

Combined with domain-specific bounds:

```text
age:        15 – 100
gpa:        0.0 – 4.0
attendance: 0 – 100
```

Values outside the effective range are capped (not removed).

### Cleaning Report Example

The cleaner generates a detailed report in the logs:

```text
==================================================
DATA CLEANING REPORT
==================================================
Final row count: 17
--- Actions Taken ---
  full_duplicates_removed: 1
  age_coerced_to_nan: 2
  age_missing_filled: 4
  age_fill_value_median: 21.0
  gpa_missing_filled: 2
  gpa_fill_value_mean: 3.22
  attendance_missing_filled: 2
  attendance_fill_value_median: 91.0
  city_missing_filled: 1
  city_fill_value_mode: Sanaa
  age_outliers_capped: 4
  gpa_outliers_capped: 2
  attendance_outliers_capped: 3
--- Descriptive Statistics ---
  age -> count=17, mean=21.41, median=21.00, std=1.28, min=20.00, max=24.00, Q1=21.00, Q3=22.00
  gpa -> count=17, mean=3.41, median=3.50, std=0.41, min=2.45, max=4.00, Q1=3.20, Q3=3.70
  attendance -> count=17, mean=90.41, median=91.00, std=5.55, min=80.50, max=100.00, Q1=88.00, Q3=93.00
--- Remaining Missing Values ---
  student_id: 1 missing
  name: 1 missing
==================================================
```

### Data Validation

After cleaning, records are validated against these rules:

```text
missing student_id    → student_id is NaN
duplicate student_id  → same ID in multiple rows
missing name          → name is empty or NaN
invalid age           → outside 15–100
invalid gpa           → outside 0.0–4.0
invalid attendance    → outside 0–100
missing city          → city is empty or NaN
```

Rejected records include a `_source` column so you can trace which data source produced the bad record.

Invalid records are not silently discarded.

They are stored separately with a `rejection_reason` column explaining why the record was rejected.

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
- Data cleaning actions (with statistics)
- Descriptive statistics (Mean, Median, Std, Q1, Q3)
- Validation results
- Merge results
- Output generation
- SQLite loading

## Testing

Run all tests:

```powershell
python -m pytest tests -v
```

Run a specific test file:

```powershell
python -m pytest tests/test_clean.py -v -s
```

### Test Coverage

| Test File | Tests | Description |
|-----------|-------|-------------|
| `test_clean.py` | 13 | Column names, text cleaning, numeric conversion, duplicates, mean/median/mode fill, outlier capping, rounding, empty DataFrames, real CSV integration |
| `test_validate.py` | 7 | Missing fields, invalid ranges, multiple rejections, duplicates, real CSV validation |
| `test_merge.py` | 5 | Multi-source merge, source priority, `_source` column in valid/rejected, empty DataFrame handling |
| `test_pipeline.py` | 2 | Full pipeline flow, rejection handling |
| `test_csv_loader.py` | 1 | CSV extraction |
| `test_csv_writer.py` | 1 | CSV output |
| `test_sqlite_loader.py` | 1 | SQLite loading |
| `test_pipeline_output.py` | 2 | Schema validation, value range validation after full pipeline |
| `test_source_merge.py` | 1 | CSV + MongoDB integration |
| `test_mongodb_loader.py` | 1 | MongoDB extraction |
| `test_api_loader.py` | 6 | DataFrame type, row count, columns, first row, null values, invalid URL |
| `test_postgres_loader.py` | 1 | PostgreSQL extraction |

## Logging

The project uses a centralized logger:

```python
from src.logger import logger
```

Log messages include timestamps and log levels.

Example:

```text
2026-10-05 17:28:20 | INFO | PostgreSQL loaded successfully: 10 rows, 6 columns
2026-10-06 03:10:00 | INFO | Age: 4 missing values filled with median = 21.0
2026-10-06 03:10:00 | INFO | GPA: 2 missing values filled with mean = 3.22
2026-10-06 03:10:00 | INFO | Column 'age': 4 outliers capped to range [19.50, 23.50]
```

## Current Pipeline Status

| Component | Status |
|-----------|--------|
| CSV Extraction | ✅ Completed |
| MongoDB Extraction | ✅ Completed |
| REST API Extraction | ✅ Completed |
| PostgreSQL Extraction | ✅ Completed |
| Fault-Tolerant Source Loading | ✅ Completed |
| Data Cleaning (9 Steps) | ✅ Completed |
| Missing Value Imputation (Mean/Median/Mode) | ✅ Completed |
| Outlier Detection (IQR) | ✅ Completed |
| Cleaning Report & Statistics | ✅ Completed |
| Data Validation (7 Rules) | ✅ Completed |
| Source Merge (Priority-Based) | ✅ Completed |
| `_source` Tracking (Valid & Rejected) | ✅ Completed |
| CSV Output | ✅ Completed |
| SQLite Output | ✅ Completed |
| Automated Tests (45 tests) | ✅ Completed |

## Future Improvements

Planned improvements include:

- Improving PostgreSQL connectivity using SQLAlchemy
- Adding data profiling dashboards
- Adding CI/CD with GitHub Actions
- Adding more data sources
- Improving pipeline configuration
- Adding a `conftest.py` for shared test fixtures

## Author

**Abdulrhman Hussin**

Student Data Engineering Project