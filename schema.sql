CREATE TABLE visits (
    id INTEGER PRIMARY KEY,
    visited_at TEXT
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
);
