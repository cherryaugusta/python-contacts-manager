import re
from datetime import datetime

from .exceptions import ValidationError

EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9\-\s\(\)]{7,20}$")


def validate_non_empty(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(f"{field_name} must not be empty.")
    return cleaned


def validate_email(email: str) -> str:
    cleaned = validate_non_empty(email, "Email").lower()
    if not EMAIL_PATTERN.match(cleaned):
        raise ValidationError("Email format is invalid.")
    return cleaned


def validate_phone(phone: str) -> str:
    cleaned = validate_non_empty(phone, "Phone")
    if not PHONE_PATTERN.match(cleaned):
        raise ValidationError("Phone format is invalid.")
    return cleaned


def validate_tags(tags: list[str]) -> list[str]:
    cleaned_tags = []
    seen = set()

    for tag in tags:
        cleaned = tag.strip().lower()
        if not cleaned:
            continue
        if len(cleaned) > 30:
            raise ValidationError("Each tag must be 30 characters or fewer.")
        if cleaned not in seen:
            seen.add(cleaned)
            cleaned_tags.append(cleaned)

    return cleaned_tags


def validate_date_iso(date_text: str, field_name: str) -> str:
    cleaned = date_text.strip()
    if not cleaned:
        return ""
    try:
        datetime.strptime(cleaned, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError(f"{field_name} must use YYYY-MM-DD format.") from exc
    return cleaned


def validate_note_content(content: str) -> str:
    cleaned = validate_non_empty(content, "Note")
    if len(cleaned) > 500:
        raise ValidationError("Note must be 500 characters or fewer.")
    return cleaned


def validate_contact_fields(
    *,
    full_name: str,
    email: str,
    phone: str,
    company: str,
    job_title: str,
    tags: list[str],
    next_follow_up: str,
) -> dict:
    validated_name = validate_non_empty(full_name, "Full name")
    validated_company = company.strip()
    validated_job_title = job_title.strip()

    if len(validated_name) > 100:
        raise ValidationError("Full name must be 100 characters or fewer.")
    if len(validated_company) > 100:
        raise ValidationError("Company must be 100 characters or fewer.")
    if len(validated_job_title) > 100:
        raise ValidationError("Job title must be 100 characters or fewer.")

    return {
        "full_name": validated_name,
        "email": validate_email(email),
        "phone": validate_phone(phone),
        "company": validated_company,
        "job_title": validated_job_title,
        "tags": validate_tags(tags),
        "next_follow_up": validate_date_iso(next_follow_up, "Next follow-up"),
    }
