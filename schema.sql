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

CREATE TABLE position_classes (
    id INTEGER PRIMARY KEY,
    position_id INTEGER REFERENCES positions,
    field TEXT,
    season TEXT
);