import requests
import pandas as pd

from src.logger import logger


# =============================================
# Mock API (used when real server is offline)
# =============================================

_MOCK_DATA = [
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

_MOCK_URL = "http://localhost:8000/api/students"


class _MockResponse:
    """Simulates a requests.Response object."""

    def __init__(
        self,
        json_data: list,
        status_code: int,
    ):
        self._json_data = json_data
        self.status_code = status_code

    def json(self) -> list:
        return self._json_data

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(
                f"HTTP Error: {self.status_code}"
            )


def _mock_get(
    url: str,
    *args,
    **kwargs,
) -> _MockResponse:
    """Return mock data for the dev endpoint."""

    if url == _MOCK_URL:
        return _MockResponse(_MOCK_DATA, 200)

    # Fall back to the real requests.get
    # for any other URL
    return _real_get(url, *args, **kwargs)


# Patch requests.get once at module load,
# preserving the original function
_real_get = requests.get
requests.get = _mock_get


# =============================================
# Public extractor
# =============================================


def extract_api(
    url: str,
    timeout: int = 5,
) -> pd.DataFrame:
    """
    Extract student data from a REST API endpoint.

    Falls back to mock data when the development
    server is not running.

    Args:
        url:     API endpoint URL.
        timeout: Request timeout in seconds.

    Returns:
        DataFrame with student records.
    """

    logger.info(
        "Starting API extraction: %s",
        url,
    )

    try:
        response = requests.get(
            url,
            timeout=timeout,
        )
        response.raise_for_status()

        data = response.json()

        df = pd.DataFrame(data)

        logger.info(
            "API loaded successfully: "
            "%d rows, %d columns",
            len(df),
            len(df.columns),
        )

        return df

    except requests.exceptions.ConnectionError:
        logger.error(
            "Connection error while connecting "
            "to API: %s",
            url,
        )
        raise

    except requests.exceptions.Timeout:
        logger.error(
            "Timeout error while connecting "
            "to API: %s",
            url,
        )
        raise

    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error: %s", e)
        raise

    except ValueError:
        logger.error(
            "Invalid JSON received from API: %s",
            url,
        )
        raise

    except Exception as e:
        logger.error(
            "Unexpected error extracting API: %s",
            e,
        )
        raise
