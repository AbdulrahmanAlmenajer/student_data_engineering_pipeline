import logging
from pathlib import Path


LOG_FILE = Path("logs/pipeline.log")

LOG_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)


logger = logging.getLogger("student_pipeline")

logger.setLevel(logging.INFO)


if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )

    console_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)