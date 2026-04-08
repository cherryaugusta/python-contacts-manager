import json
from pathlib import Path

from .exceptions import StorageError
from .models import Contact
from .utils import DEFAULT_JSON_PATH, ensure_runtime_directories


class JsonStorage:
    def __init__(self, json_path: str | Path | None = None) -> None:
        self.json_path = Path(json_path) if json_path else DEFAULT_JSON_PATH
        ensure_runtime_directories()

    def initialize(self) -> None:
        if not self.json_path.exists():
            self._write_raw({"contacts": []})

    def load_contacts(self) -> list[Contact]:
        self.initialize()
        try:
            with self.json_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            return [Contact.from_dict(item) for item in data.get("contacts", [])]
        except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise StorageError(f"Failed to load contacts from {self.json_path}") from exc

    def save_contacts(self, contacts: list[Contact]) -> None:
        payload = {"contacts": [contact.to_dict() for contact in contacts]}
        self._write_raw(payload)

    def _write_raw(self, payload: dict) -> None:
        try:
            with self.json_path.open("w", encoding="utf-8") as file:
                json.dump(payload, file, indent=2, ensure_ascii=False)
        except OSError as exc:
            raise StorageError(f"Failed to write contacts to {self.json_path}") from exc
