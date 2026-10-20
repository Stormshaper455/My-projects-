# Staff Manager

**An employee management CLI built with Python and SQLite.**

Add, view, search, update, and delete employee records from a terminal. This project demonstrates how Python functions, parameterized SQL, database constraints, and persistent storage work together in a small application.

[Source code](staffing_app.py) · [SQL schema](schema.sql) · [SQL examples](queries.sql) · [Sample session](docs/demo.md)

## Features

- Create employee records with a name, position, email, and hourly rate.
- List all employees with their IDs and formatted hourly rates.
- Search by an exact last-name match.
- Update a position and hourly rate using an employee ID.
- Delete an employee using an employee ID.
- Keep records between sessions in a local `staffing.db` file.
- Reject duplicate emails and nonnumeric hourly-rate input.
- Pass user values as SQL parameters instead of joining them into SQL strings.

## Quick start

Requires **Python 3** with the standard-library `sqlite3` module. No package installation, database server, credentials, or `.env` file is needed.

From the repository root:

```bash
cd python-sql-staff-manager
python3 staffing_app.py
```

On Windows, `py staffing_app.py` is an alternative.

The application creates `staffing.db` in your current working directory and creates the employee table automatically. Run it from the same directory each time to use the same database. You do not need to import `schema.sql` first.

```text
Staff Management System
1. Add employee
2. View employees
3. Search employees
4. Update employee
5. Delete employee
6. Exit
```

Use option **1** to add a fictional employee, **2** to view the record, and **6** to exit. See the [walkthrough](docs/demo.md) for a full example.

## Database design

The `employees` table has six columns:

| Column | SQLite type | Rule |
| --- | --- | --- |
| `id` | `INTEGER` | Automatically assigned primary key |
| `first_name` | `TEXT` | Not null |
| `last_name` | `TEXT` | Not null |
| `position` | `TEXT` | Not null |
| `email` | `TEXT` | Unique |
| `hourly_rate` | `REAL` | Not null |

The table definition is also available in [schema.sql](schema.sql). The app uses SQLite; these files are not MySQL scripts.

For a separate SQL-only demo, open an in-memory SQLite session with the optional `sqlite3` command-line tool:

```bash
sqlite3 :memory:
```

Then run:

```sql
.read schema.sql
.read queries.sql
```

The examples insert a fictional employee, read and update the record, then delete it. They run in a transaction that is rolled back at the end.

## Checks

From this project directory:

```bash
python3 -m unittest discover -s tests -v
```

The integration checks launch the real CLI against temporary databases. They cover the employee lifecycle, persistence between sessions, duplicate emails, invalid numeric input, and an apostrophe in a name. GitHub Actions runs the same checks for changes to this project.

## Scope and next steps

This is a learning project for local use with fictional records. It has no authentication or multi-user access controls. Search matches the last name exactly, and validation is currently limited to numeric input and unique emails. Planned improvements include required-field checks, nonnegative rates, and confirmation before deletion.

Local databases are excluded from Git. The repository contains source code and fictional examples; the app starts with an empty database.

---

Part of [Joshua Wilson's project portfolio](../README.md).
