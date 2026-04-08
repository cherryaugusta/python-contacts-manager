class ContactsManagerError(Exception):
    """Base exception for the contacts manager application."""


class ValidationError(ContactsManagerError):
    """Raised when user input fails validation."""


class DuplicateContactError(ContactsManagerError):
    """Raised when a contact duplicates an existing email or phone."""


class ContactNotFoundError(ContactsManagerError):
    """Raised when a contact cannot be found."""


class StorageError(ContactsManagerError):
    """Raised when storage operations fail."""
