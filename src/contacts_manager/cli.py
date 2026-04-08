import argparse
from typing import Iterable

from .exceptions import ContactsManagerError
from .services import ContactService
from .storage import JsonStorage
from .utils import parse_csv_tags, setup_logging
from .validation import validate_date_iso

logger = setup_logging()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Local contact and relationship tracking utility for small professional services teams.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("seed", help="Seed fictional demo contacts into empty storage.")

    list_parser = subparsers.add_parser("list", help="List all contacts.")
    list_parser.add_argument("--tag", default="", help="Optional tag filter.")

    add_parser = subparsers.add_parser("add", help="Add a new contact.")
    add_parser.add_argument("--full-name", required=True)
    add_parser.add_argument("--email", required=True)
    add_parser.add_argument("--phone", required=True)
    add_parser.add_argument("--company", default="")
    add_parser.add_argument("--job-title", default="")
    add_parser.add_argument("--tags", default="")
    add_parser.add_argument("--next-follow-up", default="")

    update_parser = subparsers.add_parser("update", help="Update an existing contact.")
    update_parser.add_argument("--contact-id", required=True)
    update_parser.add_argument("--full-name", required=True)
    update_parser.add_argument("--email", required=True)
    update_parser.add_argument("--phone", required=True)
    update_parser.add_argument("--company", default="")
    update_parser.add_argument("--job-title", default="")
    update_parser.add_argument("--tags", default="")
    update_parser.add_argument("--next-follow-up", default="")

    delete_parser = subparsers.add_parser("delete", help="Delete a contact.")
    delete_parser.add_argument("--contact-id", required=True)

    search_parser = subparsers.add_parser("search", help="Search contacts.")
    search_parser.add_argument("--query", default="")
    search_parser.add_argument("--tag", default="")

    note_parser = subparsers.add_parser("add-note", help="Add a note to a contact.")
    note_parser.add_argument("--contact-id", required=True)
    note_parser.add_argument("--note", required=True)

    due_parser = subparsers.add_parser("due-followups", help="List due follow-ups.")
    due_parser.add_argument("--date", required=True)

    return parser


def print_contacts(contacts: Iterable) -> None:
    contacts = list(contacts)
    if not contacts:
        print("No contacts found.")
        return

    for contact in contacts:
        print("-" * 80)
        print(f"ID: {contact.contact_id}")
        print(f"Name: {contact.full_name}")
        print(f"Email: {contact.email}")
        print(f"Phone: {contact.phone}")
        print(f"Company: {contact.company}")
        print(f"Job Title: {contact.job_title}")
        print(f"Tags: {', '.join(contact.tags) if contact.tags else 'None'}")
        print(f"Next Follow-Up: {contact.next_follow_up or 'None'}")
        print(f"Created: {contact.created_at}")
        print(f"Updated: {contact.updated_at}")
        if contact.notes:
            print("Notes:")
            for note in contact.notes:
                print(f"  - [{note.note_id}] {note.created_at} | {note.content}")
        else:
            print("Notes: None")
    print("-" * 80)
    print(f"Total contacts: {len(contacts)}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    storage = JsonStorage()
    service = ContactService(storage)

    try:
        if args.command == "seed":
            seeded = service.seed_demo_contacts()
            logger.info("Seed command executed.")
            print(f"Storage seeded. Total contacts available: {len(seeded)}")

        elif args.command == "list":
            contacts = service.list_contacts()
            if args.tag:
                contacts = [
                    contact
                    for contact in contacts
                    if args.tag.strip().lower() in contact.tags
                ]
            print_contacts(contacts)

        elif args.command == "add":
            contact = service.create_contact(
                full_name=args.full_name,
                email=args.email,
                phone=args.phone,
                company=args.company,
                job_title=args.job_title,
                tags=parse_csv_tags(args.tags),
                next_follow_up=args.next_follow_up,
            )
            logger.info("Contact added: %s", contact.contact_id)
            print(f"Contact created successfully: {contact.contact_id}")

        elif args.command == "update":
            contact = service.update_contact(
                contact_id=args.contact_id,
                full_name=args.full_name,
                email=args.email,
                phone=args.phone,
                company=args.company,
                job_title=args.job_title,
                tags=parse_csv_tags(args.tags),
                next_follow_up=args.next_follow_up,
            )
            logger.info("Contact updated: %s", contact.contact_id)
            print(f"Contact updated successfully: {contact.contact_id}")

        elif args.command == "delete":
            service.delete_contact(args.contact_id)
            logger.info("Contact deleted: %s", args.contact_id)
            print(f"Contact deleted successfully: {args.contact_id}")

        elif args.command == "search":
            contacts = service.search_contacts(query=args.query, tag=args.tag)
            print_contacts(contacts)

        elif args.command == "add-note":
            note = service.add_note(args.contact_id, args.note)
            logger.info("Note added: %s", note.note_id)
            print(f"Note added successfully: {note.note_id}")

        elif args.command == "due-followups":
            validated_date = validate_date_iso(args.date, "Date")
            contacts = service.due_followups(validated_date)
            print_contacts(contacts)

    except ContactsManagerError as exc:
        logger.error("Application error: %s", exc)
        print(f"ERROR: {exc}")
        raise SystemExit(1)
