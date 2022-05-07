import re
import sqlite3
import os
from dotenv import load_dotenv
from db_utils import select, execute;

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_budget_categories():
    return select("""
        SELECT cp.id, cp.pattern, cp.category_id, c.label AS category_label
        FROM category_patterns cp
        LEFT OUTER JOIN categories c ON cp.category_id = c.id
        ORDER BY c.label, cp.pattern
        """)

def create_budget_categories(category, budget, month, year):
    # TODO
    execute("""
        DELETE FROM budget_categories
        VALUES (?, ?);
        """, (pattern,category,))
    execute("""
        INSERT INTO budget_categories (pattern, category_id)
        VALUES (?, ?);
        """, (pattern,category,))

def delete_budget_categories(id):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("PRAGMA foreign_keys = ON;")
  cursor.execute("""
    DELETE FROM budget_categories
    WHERE id = ?;
    """, (id,))
  db.commit()
  cursor.close()
  db.close()
