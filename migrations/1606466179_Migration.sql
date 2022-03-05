CREATE TABLE categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	label TEXT NOT NULL
);

CREATE TABLE category_patterns (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	pattern TEXT NOT NULL,
	category_id INTEGER NOT NULL
);

CREATE TABLE simulations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	label TEXT NOT NULL
);

CREATE TABLE budget_categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	category_id INTEGER NOT NULL,
	year INTEGER NULL,
	month INTEGER NULL,
	amount REAL DEFAULT 0
);

CREATE TABLE transactions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	year INTEGER NOT NULL,
	month INTEGER NOT NULL,
	day INTEGER NOT NULL,
	category_id INTEGER NULL,
	simulation_id INTEGER NULL,
	label TEXT NOT NULL,
	amount REAL DEFAULT 0,
	hash TEXT NOT NULL
);

CREATE INDEX transactions_year_IDX ON transactions ("year");
CREATE INDEX transactions_month_IDX ON transactions ("month");
CREATE INDEX transactions_day_IDX ON transactions ("day");
CREATE INDEX transactions_hash_IDX ON transactions (hash);
CREATE INDEX transactions_year_month_IDX ON transactions ("year","month");