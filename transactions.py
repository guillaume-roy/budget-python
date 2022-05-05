import re
import sqlite3
import os
from dotenv import load_dotenv
from db_utils import select, execute;

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_transactions():
    return select("""
        SELECT t.id, t.year, t.month, t.day, t.category_pattern_id, t.simulation_id, t.label, t.amount, t.hash, COALESCE(c2.label, c.label) AS category_label, COALESCE(c2.id, c.id) as category_id
        FROM transactions t
        LEFT OUTER JOIN category_patterns cp ON t.category_pattern_id = cp.id
        LEFT OUTER JOIN categories c ON cp.category_id = c.id
        LEFT OUTER JOIN categories c2 ON t.category_id = c2.id
        ORDER BY t.year DESC, t.month DESC, t.day DESC;
        """)

def get_transactions_none():
    return select("""
        SELECT t.id, t.year, t.month, t.day, t.category_pattern_id, t.simulation_id, t.label, t.amount, t.hash, COALESCE(c2.label, c.label) AS category_label, COALESCE(c2.id, c.id) as category_id
        FROM transactions t
        LEFT OUTER JOIN category_patterns cp ON t.category_pattern_id = cp.id
        LEFT OUTER JOIN categories c ON cp.category_id = c.id
        LEFT OUTER JOIN categories c2 ON t.category_id = c2.id
        WHERE COALESCE(c2.id, c.id) IS NULL
        ORDER BY t.year DESC, t.month DESC, t.day DESC;
        """)

def assign_category(transaction_id, category):
    if(category == "none"):
        execute("""
            UPDATE transactions
            SET category_id = NULL, category_pattern_id = NULL
            WHERE id = ?;
            """, (transaction_id,))
    else:
        execute("UPDATE transactions SET category_pattern_id = NULL, category_id=? WHERE id=?",(category,transaction_id,))
