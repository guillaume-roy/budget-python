PRAGMA foreign_keys = ON;

CREATE TABLE categories (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	label TEXT NOT NULL
);

CREATE TABLE category_patterns (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	pattern TEXT NOT NULL,
	category_id INTEGER NOT NULL,

    CONSTRAINT FK_CATEGORY_PATTERNS_CATEGORY_ID
    FOREIGN KEY (category_id)
    REFERENCES categories (id)
    ON DELETE CASCADE
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
	amount REAL DEFAULT 0,

    CONSTRAINT FK_BUDGET_CATEGORIES_CATEGORY_ID
    FOREIGN KEY (category_id)
    REFERENCES categories (id)
    ON DELETE CASCADE
);

CREATE TABLE transactions (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	year INTEGER NOT NULL,
	month INTEGER NOT NULL,
	day INTEGER NOT NULL,
	category_pattern_id INTEGER NULL,
    category_id INTEGER NULL,
	simulation_id INTEGER NULL,
	label TEXT NOT NULL,
	amount REAL DEFAULT 0,
	hash TEXT NOT NULL,

    CONSTRAINT FK_TRANSACTIONS_CATEGORY_PATTERN_ID
    FOREIGN KEY (category_pattern_id)
    REFERENCES category_patterns (id)
    ON DELETE SET NULL,

    CONSTRAINT FK_TRANSACTIONS_SIMULATION_ID
    FOREIGN KEY (simulation_id)
    REFERENCES simulations (id)
    ON DELETE CASCADE,

    CONSTRAINT FK_TRANSACTIONS_CATEGORY_ID
    FOREIGN KEY (category_id)
    REFERENCES categories(id)
    ON DELETE SET NULL
);

CREATE INDEX transactions_year_IDX ON transactions ("year");
CREATE INDEX transactions_month_IDX ON transactions ("month");
CREATE INDEX transactions_day_IDX ON transactions ("day");
CREATE INDEX transactions_hash_IDX ON transactions (hash);
CREATE INDEX transactions_year_month_IDX ON transactions ("year","month");
