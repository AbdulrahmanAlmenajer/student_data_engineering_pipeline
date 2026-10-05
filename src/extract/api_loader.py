
import requests
import pandas as pd

from src.logger import logger


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"HTTP Error: {self.status_code}"
            )


def mock_get(url, *args, **kwargs):
    if url == "http://localhost:8000/api/students":
        data = [
            {
                "student_id": "1001",
                "name": "Ahmed",
                "age": 22,
                "gpa": 3.8,
                "attendance": 95,
                "city": "Sanaa",
            },
            {
                "student_id": "1002",
                "name": "Mohammed",
                "age": 21,
                "gpa": 3.2,
                "attendance": 85,
                "city": "Taiz",
            },
            {
                "student_id": "1003",
                "name": "Khaled",
                "age": 23,
                "gpa": 2.5,
                "attendance": 70,
                "city": "Ibb",
            },
            {
                "student_id": "1004",
                "name": "Ali",
                "age": 20,
                "gpa": 4.5,
                "attendance": 90,
                "city": "Sanaa",
            },
            {
                "student_id": "1005",
                "name": "Salma",
                "age": 19,
                "gpa": None,
                "attendance": None,
                "city": "Dhamar",
            },
        ]
        return MockResponse(data, 200)

    return requests.original_get(url, *args, **kwargs)


if not hasattr(requests, "original_get"):
    requests.original_get = requests.get

requests.get = mock_get


def extract_api(url, timeout=5):
    logger.info(f"Starting API extraction: {url}")

    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data)

        logger.info(
            f"API loaded successfully: {len(df)} rows, {len(df.columns)} columns"
        )

        return df

    except requests.exceptions.ConnectionError:
        logger.error("Connection Error while connecting to API")
        raise

    except requests.exceptions.Timeout:
        logger.error("Timeout Error while connecting to API")
        raise

    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e}")
        raise

    except ValueError:
        logger.error("Invalid JSON received from API")
        raise

    except Exception as e:
        logger.error(f"Error extracting API: {e}")
        raise
