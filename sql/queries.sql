-- Insert a contact
INSERT INTO contacts (
    contact_id,
    full_name,
    email,
    phone,
    company,
    job_title,
    next_follow_up,
    created_at,
    updated_at
) VALUES (
    'con_a1b2c3d4e5',
    'Amina Rahman',
    'amina.rahman@northbridgeadvisory.co.uk',
    '+44 20 7946 0101',
    'Northbridge Advisory',
    'Operations Manager',
    '2026-04-15',
    NOW(),
    NOW()
);

-- Read all contacts
SELECT
    contact_id,
    full_name,
    email,
    phone,
    company,
    job_title,
    next_follow_up,
    created_at,
    updated_at
FROM contacts
ORDER BY full_name ASC;

-- Read one contact by ID
SELECT *
FROM contacts
WHERE contact_id = 'con_a1b2c3d4e5';

-- Update a contact
UPDATE contacts
SET
    company = 'Northbridge Advisory Ltd',
    job_title = 'Senior Operations Manager',
    updated_at = NOW()
WHERE contact_id = 'con_a1b2c3d4e5';

-- Delete a contact
DELETE FROM contacts
WHERE contact_id = 'con_a1b2c3d4e5';

-- Insert a note
INSERT INTO contact_notes (
    note_id,
    contact_id,
    content,
    created_at
) VALUES (
    'note_12345abcde',
    'con_a1b2c3d4e5',
    'Requested pricing deck after introduction call.',
    NOW()
);

-- Search contacts by name, email, company, or phone
SELECT *
FROM contacts
WHERE
    full_name ILIKE '%amina%'
    OR email ILIKE '%amina%'
    OR company ILIKE '%northbridge%'
    OR phone ILIKE '%0101%'
ORDER BY full_name ASC;

-- Find contacts with follow-ups due on or before a date
SELECT
    contact_id,
    full_name,
    email,
    company,
    next_follow_up
FROM contacts
WHERE next_follow_up IS NOT NULL
  AND next_follow_up <= DATE '2026-04-15'
ORDER BY next_follow_up ASC, full_name ASC;

-- Insert tags
INSERT INTO tags (tag_name) VALUES ('client')
ON CONFLICT (tag_name) DO NOTHING;

INSERT INTO tags (tag_name) VALUES ('priority')
ON CONFLICT (tag_name) DO NOTHING;

-- Link tags to a contact
INSERT INTO contact_tags (contact_id, tag_id)
SELECT 'con_a1b2c3d4e5', tag_id
FROM tags
WHERE tag_name IN ('client', 'priority');

-- View contacts with their tags
SELECT
    c.contact_id,
    c.full_name,
    c.email,
    c.company,
    t.tag_name
FROM contacts c
JOIN contact_tags ct ON c.contact_id = ct.contact_id
JOIN tags t ON ct.tag_id = t.tag_id
ORDER BY c.full_name, t.tag_name;

-- View contacts with notes
SELECT
    c.contact_id,
    c.full_name,
    c.email,
    n.note_id,
    n.content,
    n.created_at
FROM contacts c
LEFT JOIN contact_notes n ON c.contact_id = n.contact_id
ORDER BY c.full_name, n.created_at DESC;

-- Find contacts tagged as client
SELECT
    c.contact_id,
    c.full_name,
    c.email,
    c.company
FROM contacts c
JOIN contact_tags ct ON c.contact_id = ct.contact_id
JOIN tags t ON ct.tag_id = t.tag_id
WHERE t.tag_name = 'client'
ORDER BY c.full_name ASC;

-- Count notes per contact
SELECT
    c.contact_id,
    c.full_name,
    COUNT(n.note_id) AS note_count
FROM contacts c
LEFT JOIN contact_notes n ON c.contact_id = n.contact_id
GROUP BY c.contact_id, c.full_name
ORDER BY note_count DESC, c.full_name ASC;
