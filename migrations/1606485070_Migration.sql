CREATE INDEX transactions_year_IDX ON transactions ("year");
CREATE INDEX transactions_month_IDX ON transactions ("month");
CREATE INDEX transactions_day_IDX ON transactions ("day");
CREATE INDEX transactions_hash_IDX ON transactions (hash);
CREATE INDEX transactions_year_month_IDX ON transactions ("year","month");
