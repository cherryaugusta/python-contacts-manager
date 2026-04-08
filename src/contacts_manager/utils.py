import json
import logging
import os
import uuid
from datetime import datetime, UTC
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
LOGS_DIR = ROOT_DIR / "logs"
DEFAULT_JSON_PATH = DATA_DIR / "contacts.json"
DEFAULT_LOG_PATH = LOGS_DIR / "contacts_manager.log"


def ensure_runtime_directories() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging() -> logging.Logger:
    ensure_runtime_directories()

    logger = logging.getLogger("contacts_manager")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(DEFAULT_LOG_PATH, encoding="utf-8")
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def parse_csv_tags(raw_tags: str | None) -> list[str]:
    if not raw_tags:
        return []
    return [part.strip() for part in raw_tags.split(",")]


def pretty_json(data: dict | list) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False)


def file_exists(path: os.PathLike | str) -> bool:
    return Path(path).exists()
