import re
import sqlite3
import os
from dotenv import load_dotenv
from db_utils import select, execute

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_by_month(year, month):
    # TODO
    return select("""
        select COALESCE(c2.label, c.label) as category_label, SUM(t.amount) as total
        from transactions t
        LEFT OUTER JOIN category_patterns cp on t.category_pattern_id = cp.id
        LEFT OUTER JOIN categories c on cp.category_id = c.id
        LEFT OUTER JOIN categories c2 ON t.category_id = c2.id
        WHERE t.month = ? and t.year = ?
        GROUP BY COALESCE(c2.label, c.label)
        """, (int(year), int(month),))
