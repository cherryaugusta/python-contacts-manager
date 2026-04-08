# Portfolio Case Study: Python Contacts Manager

## Project summary

Python Contacts Manager is a command-line application for managing professional contacts, notes, tags, and follow-up dates locally. It is designed for small teams or individual operators who need a lightweight contact workflow without the overhead of a full CRM.

## Project goal

The goal of this project was to build a Python repository that demonstrates:

- clean command-line application structure
- input validation and normalization
- duplicate prevention
- file-based persistence
- relational SQL design thinking
- automated testing
- clear technical documentation
- realistic execution evidence through screenshots

## Problem context

Small teams often need a reliable way to track contacts, notes, and follow-up dates, but a spreadsheet is often too fragile and a full CRM can be too heavy for the workflow. This project explores a maintainable middle ground: a local utility that provides structured data handling, predictable commands, and clear separation between user interaction, business logic, and storage.

## Solution design

The application uses a responsibility-based structure:

- CLI layer for command parsing and user interaction
- service layer for business rules
- validation layer for input quality and normalization
- storage layer for JSON persistence
- model layer for structured contact and note data
- SQL files to show how the same domain maps to a relational schema

## Core features

- add, update, list, search, and delete contacts
- duplicate prevention by email and phone
- note support for relationship context
- tag support for filtering and categorization
- follow-up date tracking
- fictional demo data seeding
- custom exceptions and controlled CLI errors
- automated tests for core workflows

## Technical decisions

### Why JSON persistence

JSON was chosen for the running application because:

- it keeps local execution simple
- it avoids infrastructure overhead
- it still supports strong separation of concerns
- it makes storage logic easy to test

### Why include SQL separately

Although the running application uses JSON storage, the repository also includes relational SQL assets to demonstrate schema and query design. These files show:

- table design
- primary keys
- unique constraints
- foreign keys
- indexes
- CRUD queries
- joins across contacts, notes, and tags

### Why a service layer

Business rules such as duplicate prevention, note creation, and follow-up filtering belong outside the CLI and outside the storage layer. This improves readability, maintainability, and testability.

## Validation and error handling

The project validates:

- required full name values
- email format
- phone format
- follow-up date format
- note content length
- tag normalization and de-duplication

The project also rejects duplicate contacts when an email address or phone number already exists. Custom exceptions are used to keep CLI error messages clear and controlled.

## Testing approach

The test suite verifies:

- validation behavior
- storage initialization and persistence
- duplicate prevention
- note creation
- delete behavior
- due follow-up filtering

This ensures the project demonstrates not only implementation but also verification of core behavior.

## Example fictional data

The demo workflow uses clearly fictional records such as:

- Sigrid Tomoe Haldorsen at Aurora Ledger Atelier
- Leif Katsumi Thoresen at Fjord Kestrel Counsel
- Ingrid Suzu Bjornsdatter at Mist Harbor Metrics
- Eirik Nozomi Valdsen at Pale Summit Works

Emails use reserved example domains and phone numbers are clearly non-real placeholder values.

## Extension paths

Possible future improvements include:

- replacing JSON storage with SQLite or PostgreSQL
- adding import and export commands
- exposing the service layer through a REST API
- introducing richer search and filtering options
- packaging the CLI as an installable Python tool

## Outcome

The final result is a complete Python CLI project with layered structure, validation, JSON persistence, SQL assets, automated tests, screenshots, and coherent documentation. It is small enough to understand end to end, while still showing practical software engineering judgment in structure, data handling, testing, and repository presentation.
