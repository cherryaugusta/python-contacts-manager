import pytest

from src.contacts_manager.exceptions import ValidationError
from src.contacts_manager.validation import (
    validate_contact_fields,
    validate_date_iso,
    validate_email,
    validate_note_content,
    validate_phone,
)


def test_validate_email_accepts_valid_email():
    assert validate_email("USER@example.com") == "user@example.com"


def test_validate_email_rejects_invalid_email():
    with pytest.raises(ValidationError):
        validate_email("invalid-email")


def test_validate_phone_rejects_invalid_phone():
    with pytest.raises(ValidationError):
        validate_phone("abc")


def test_validate_date_iso_accepts_valid_date():
    assert validate_date_iso("2026-04-15", "Next follow-up") == "2026-04-15"


def test_validate_date_iso_rejects_bad_date():
    with pytest.raises(ValidationError):
        validate_date_iso("15-04-2026", "Next follow-up")


def test_validate_note_content_rejects_empty_string():
    with pytest.raises(ValidationError):
        validate_note_content("   ")


def test_validate_contact_fields_normalizes_and_validates():
    result = validate_contact_fields(
        full_name="  Jane Smith  ",
        email="JANE@Example.com",
        phone="+44 20 7000 0000",
        company="Acme Ltd",
        job_title="Director",
        tags=["Client", "vip", "Client"],
        next_follow_up="2026-04-20",
    )

    assert result["full_name"] == "Jane Smith"
    assert result["email"] == "jane@example.com"
    assert result["tags"] == ["client", "vip"]
