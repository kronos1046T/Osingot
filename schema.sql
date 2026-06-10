CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    stock_name TEXT NOT NULL,
    ex_dividend_date TEXT,
    record_date TEXT,
    payment_date TEXT,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    position_id INTEGER,
    user_id INTEGER,
    content TEXT,
    FOREIGN KEY (position_id) REFERENCES positions(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    type TEXT,
    value TEXT
);

CREATE TABLE position_classes (
    id INTEGER PRIMARY KEY,
    position_id INTEGER,
    type TEXT,
    value TEXT
);