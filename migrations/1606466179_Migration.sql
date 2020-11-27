CREATE TABLE transactions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	year INTEGER NOT NULL,
	month INTEGER NOT NULL,
	day INTEGER NOT NULL,
	label TEXT NOT NULL,
	debit REAL DEFAULT 0,
	credit REAL DEFAULT 0,
	hash TEXT NOT NULL
);