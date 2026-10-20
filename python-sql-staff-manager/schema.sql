-- Reference schema. The Python app creates this table automatically.
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    position TEXT NOT NULL,
    email TEXT UNIQUE,
    hourly_rate REAL NOT NULL
);
