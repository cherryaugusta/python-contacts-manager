from __future__ import annotations

from datetime import datetime

from .exceptions import ContactNotFoundError, DuplicateContactError
from .models import Contact, ContactNote
from .storage import JsonStorage
from .utils import generate_id, utc_now_iso
from .validation import validate_contact_fields, validate_note_content


class ContactService:
    def __init__(self, storage: JsonStorage) -> None:
        self.storage = storage

    def list_contacts(self) -> list[Contact]:
        contacts = self.storage.load_contacts()
        return sorted(contacts, key=lambda c: c.full_name.lower())

    def get_contact(self, contact_id: str) -> Contact:
        contacts = self.storage.load_contacts()
        for contact in contacts:
            if contact.contact_id == contact_id:
                return contact
        raise ContactNotFoundError(f"Contact '{contact_id}' was not found.")

    def create_contact(
        self,
        *,
        full_name: str,
        email: str,
        phone: str,
        company: str = "",
        job_title: str = "",
        tags: list[str] | None = None,
        next_follow_up: str = "",
    ) -> Contact:
        tags = tags or []
        validated = validate_contact_fields(
            full_name=full_name,
            email=email,
            phone=phone,
            company=company,
            job_title=job_title,
            tags=tags,
            next_follow_up=next_follow_up,
        )

        contacts = self.storage.load_contacts()
        self._ensure_no_duplicates(
            contacts,
            email=validated["email"],
            phone=validated["phone"],
        )

        now = utc_now_iso()
        contact = Contact(
            contact_id=generate_id("con"),
            full_name=validated["full_name"],
            email=validated["email"],
            phone=validated["phone"],
            company=validated["company"],
            job_title=validated["job_title"],
            tags=validated["tags"],
            notes=[],
            next_follow_up=validated["next_follow_up"],
            created_at=now,
            updated_at=now,
        )

        contacts.append(contact)
        self.storage.save_contacts(contacts)
        return contact

    def update_contact(
        self,
        *,
        contact_id: str,
        full_name: str,
        email: str,
        phone: str,
        company: str = "",
        job_title: str = "",
        tags: list[str] | None = None,
        next_follow_up: str = "",
    ) -> Contact:
        tags = tags or []
        validated = validate_contact_fields(
            full_name=full_name,
            email=email,
            phone=phone,
            company=company,
            job_title=job_title,
            tags=tags,
            next_follow_up=next_follow_up,
        )

        contacts = self.storage.load_contacts()
        target = None
        for contact in contacts:
            if contact.contact_id == contact_id:
                target = contact
                break

        if target is None:
            raise ContactNotFoundError(f"Contact '{contact_id}' was not found.")

        self._ensure_no_duplicates(
            contacts,
            email=validated["email"],
            phone=validated["phone"],
            exclude_contact_id=contact_id,
        )

        target.full_name = validated["full_name"]
        target.email = validated["email"]
        target.phone = validated["phone"]
        target.company = validated["company"]
        target.job_title = validated["job_title"]
        target.tags = validated["tags"]
        target.next_follow_up = validated["next_follow_up"]
        target.updated_at = utc_now_iso()

        self.storage.save_contacts(contacts)
        return target

    def delete_contact(self, contact_id: str) -> None:
        contacts = self.storage.load_contacts()
        filtered = [contact for contact in contacts if contact.contact_id != contact_id]

        if len(filtered) == len(contacts):
            raise ContactNotFoundError(f"Contact '{contact_id}' was not found.")

        self.storage.save_contacts(filtered)

    def search_contacts(self, query: str = "", tag: str = "") -> list[Contact]:
        contacts = self.storage.load_contacts()
        q = query.strip().lower()
        tag_value = tag.strip().lower()

        results = []
        for contact in contacts:
            searchable_text = " ".join(
                [
                    contact.contact_id,
                    contact.full_name,
                    contact.email,
                    contact.phone,
                    contact.company,
                    contact.job_title,
                    " ".join(contact.tags),
                    " ".join(note.content for note in contact.notes),
                ]
            ).lower()

            matches_query = not q or q in searchable_text
            matches_tag = not tag_value or tag_value in contact.tags

            if matches_query and matches_tag:
                results.append(contact)

        return sorted(results, key=lambda c: c.full_name.lower())

    def add_note(self, contact_id: str, content: str) -> ContactNote:
        validated_note = validate_note_content(content)
        contacts = self.storage.load_contacts()

        for contact in contacts:
            if contact.contact_id == contact_id:
                note = ContactNote(
                    note_id=generate_id("note"),
                    content=validated_note,
                    created_at=utc_now_iso(),
                )
                contact.notes.append(note)
                contact.updated_at = utc_now_iso()
                self.storage.save_contacts(contacts)
                return note

        raise ContactNotFoundError(f"Contact '{contact_id}' was not found.")

    def due_followups(self, on_or_before: str) -> list[Contact]:
        cutoff = datetime.strptime(on_or_before, "%Y-%m-%d").date()
        contacts = self.storage.load_contacts()

        due = []
        for contact in contacts:
            if contact.next_follow_up:
                follow_up_date = datetime.strptime(
                    contact.next_follow_up, "%Y-%m-%d"
                ).date()
                if follow_up_date <= cutoff:
                    due.append(contact)

        return sorted(due, key=lambda c: (c.next_follow_up, c.full_name.lower()))

    def seed_demo_contacts(self) -> list[Contact]:
        contacts = self.storage.load_contacts()
        if contacts:
            return contacts

        seeded = [
            self.create_contact(
                full_name="Sigrid Tomoe Haldorsen",
                email="sigrid.tomoe.haldorsen@example.com",
                phone="+00 0000 000001",
                company="Aurora Ledger Atelier",
                job_title="Operations Manager",
                tags=["client", "priority"],
                next_follow_up="2026-04-15",
            ),
            self.create_contact(
                full_name="Leif Katsumi Thoresen",
                email="leif.katsumi.thoresen@example.com",
                phone="+00 0000 000002",
                company="Fjord Kestrel Counsel",
                job_title="Partner",
                tags=["prospect", "legal"],
                next_follow_up="2026-04-10",
            ),
            self.create_contact(
                full_name="Ingrid Suzu Bjornsdatter",
                email="ingrid.suzu.bjornsdatter@example.com",
                phone="+00 0000 000003",
                company="Mist Harbor Metrics",
                job_title="Account Director",
                tags=["client", "finance"],
                next_follow_up="2026-04-12",
            ),
        ]

        self.add_note(seeded[0].contact_id, "Intro call completed. Requested pricing summary.")
        self.add_note(seeded[1].contact_id, "Met during an industry networking session.")
        self.add_note(seeded[2].contact_id, "Needs quarterly follow-up on reporting support.")

        return self.storage.load_contacts()

    def _ensure_no_duplicates(
        self,
        contacts: list[Contact],
        *,
        email: str,
        phone: str,
        exclude_contact_id: str | None = None,
    ) -> None:
        for contact in contacts:
            if exclude_contact_id and contact.contact_id == exclude_contact_id:
                continue
            if contact.email.lower() == email.lower():
                raise DuplicateContactError(
                    f"Duplicate detected: email '{email}' already exists."
                )
            if contact.phone.strip() == phone.strip():
                raise DuplicateContactError(
                    f"Duplicate detected: phone '{phone}' already exists."
                )
