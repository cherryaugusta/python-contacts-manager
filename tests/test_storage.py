from pathlib import Path

from src.contacts_manager.models import Contact
from src.contacts_manager.storage import JsonStorage


def test_storage_initializes_and_saves_contacts(tmp_path: Path):
    json_path = tmp_path / "contacts.json"
    storage = JsonStorage(json_path)

    storage.initialize()
    assert json_path.exists()

    contacts = [
        Contact(
            contact_id="con_123",
            full_name="Alice Brown",
            email="alice@example.com",
            phone="+44 20 7000 0001",
            company="Example Co",
            job_title="Consultant",
            tags=["client"],
            notes=[],
            next_follow_up="2026-04-18",
            created_at="2026-04-07T10:00:00Z",
            updated_at="2026-04-07T10:00:00Z",
        )
    ]

    storage.save_contacts(contacts)
    loaded = storage.load_contacts()

    assert len(loaded) == 1
    assert loaded[0].full_name == "Alice Brown"
    assert loaded[0].email == "alice@example.com"
