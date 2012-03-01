
CREATE TABLE greeting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_on TIMESTAMP NOT NULL,
    author TEXT,
    message TEXT NOT NULL
);
