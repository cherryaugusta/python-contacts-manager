import pytest

from src.contacts_manager.exceptions import (
    ContactNotFoundError,
    DuplicateContactError,
)
from src.contacts_manager.services import ContactService
from src.contacts_manager.storage import JsonStorage


@pytest.fixture
def service(tmp_path):
    storage = JsonStorage(tmp_path / "contacts.json")
    return ContactService(storage)


def test_create_contact_and_list(service):
    created = service.create_contact(
        full_name="Michael Green",
        email="michael.green@example.com",
        phone="+44 20 7000 0002",
        company="Green Advisory",
        job_title="Advisor",
        tags=["prospect", "finance"],
        next_follow_up="2026-04-22",
    )

    contacts = service.list_contacts()

    assert len(contacts) == 1
    assert contacts[0].contact_id == created.contact_id
    assert contacts[0].email == "michael.green@example.com"


def test_duplicate_email_is_rejected(service):
    service.create_contact(
        full_name="Person One",
        email="dup@example.com",
        phone="+44 20 7000 0003",
        company="A",
        job_title="A",
        tags=[],
        next_follow_up="",
    )

    with pytest.raises(DuplicateContactError):
        service.create_contact(
            full_name="Person Two",
            email="dup@example.com",
            phone="+44 20 7000 0004",
            company="B",
            job_title="B",
            tags=[],
            next_follow_up="",
        )


def test_add_note_to_contact(service):
    created = service.create_contact(
        full_name="Sarah White",
        email="sarah.white@example.com",
        phone="+44 20 7000 0005",
        company="White Legal",
        job_title="Manager",
        tags=["legal"],
        next_follow_up="2026-04-17",
    )

    note = service.add_note(created.contact_id, "Followed up after onboarding call.")
    contact = service.get_contact(created.contact_id)

    assert note.content == "Followed up after onboarding call."
    assert len(contact.notes) == 1


def test_delete_contact(service):
    created = service.create_contact(
        full_name="Delete Me",
        email="delete.me@example.com",
        phone="+44 20 7000 0006",
        company="Delete Co",
        job_title="Lead",
        tags=[],
        next_follow_up="",
    )

    service.delete_contact(created.contact_id)

    with pytest.raises(ContactNotFoundError):
        service.get_contact(created.contact_id)


def test_due_followups(service):
    service.create_contact(
        full_name="Due Contact",
        email="due@example.com",
        phone="+44 20 7000 0007",
        company="Due Ltd",
        job_title="Director",
        tags=["client"],
        next_follow_up="2026-04-10",
    )
    service.create_contact(
        full_name="Later Contact",
        email="later@example.com",
        phone="+44 20 7000 0008",
        company="Later Ltd",
        job_title="Director",
        tags=["client"],
        next_follow_up="2026-04-25",
    )

    due = service.due_followups("2026-04-12")

    assert len(due) == 1
    assert due[0].email == "due@example.com"
