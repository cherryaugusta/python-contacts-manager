from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import List


@dataclass
class ContactNote:
    note_id: str
    content: str
    created_at: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ContactNote":
        return cls(
            note_id=data["note_id"],
            content=data["content"],
            created_at=data["created_at"],
        )


@dataclass
class Contact:
    contact_id: str
    full_name: str
    email: str
    phone: str
    company: str
    job_title: str
    tags: List[str] = field(default_factory=list)
    notes: List[ContactNote] = field(default_factory=list)
    next_follow_up: str = ""
    created_at: str = ""
    updated_at: str = ""

    def to_dict(self) -> dict:
        data = asdict(self)
        data["notes"] = [note.to_dict() for note in self.notes]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Contact":
        return cls(
            contact_id=data["contact_id"],
            full_name=data["full_name"],
            email=data["email"],
            phone=data["phone"],
            company=data.get("company", ""),
            job_title=data.get("job_title", ""),
            tags=data.get("tags", []),
            notes=[ContactNote.from_dict(note) for note in data.get("notes", [])],
            next_follow_up=data.get("next_follow_up", ""),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )
