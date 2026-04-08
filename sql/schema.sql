-- Contacts Manager relational schema
-- Target database: PostgreSQL

DROP TABLE IF EXISTS contact_tags;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS contact_notes;
DROP TABLE IF EXISTS contacts;

CREATE TABLE contacts (
    contact_id VARCHAR(32) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL UNIQUE,
    company VARCHAR(100),
    job_title VARCHAR(100),
    next_follow_up DATE,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

CREATE TABLE contact_notes (
    note_id VARCHAR(32) PRIMARY KEY,
    contact_id VARCHAR(32) NOT NULL,
    content VARCHAR(500) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT fk_contact_notes_contact
        FOREIGN KEY (contact_id)
        REFERENCES contacts(contact_id)
        ON DELETE CASCADE
);

CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE contact_tags (
    contact_id VARCHAR(32) NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (contact_id, tag_id),
    CONSTRAINT fk_contact_tags_contact
        FOREIGN KEY (contact_id)
        REFERENCES contacts(contact_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_contact_tags_tag
        FOREIGN KEY (tag_id)
        REFERENCES tags(tag_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_contacts_full_name ON contacts(full_name);
CREATE INDEX idx_contacts_company ON contacts(company);
CREATE INDEX idx_contacts_next_follow_up ON contacts(next_follow_up);
CREATE INDEX idx_contact_notes_contact_id ON contact_notes(contact_id);
