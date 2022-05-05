import re
import sqlite3
import os
from dotenv import load_dotenv
from db_utils import select, execute;

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_categories_patterns():
    return select("""
        SELECT cp.id, cp.pattern, cp.category_id, c.label AS category_label
        FROM category_patterns cp
        LEFT OUTER JOIN categories c ON cp.category_id = c.id
        ORDER BY c.label, cp.pattern
        """)

def create_pattern(pattern, category):
    execute("""
        INSERT INTO category_patterns (pattern, category_id)
        VALUES (?, ?);
        """, (pattern,category,))

def delete_pattern(pattern_id):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("PRAGMA foreign_keys = ON;")
  cursor.execute("""
    DELETE FROM category_patterns
    WHERE id = ?;
    """, (pattern_id,))
  db.commit()
  cursor.close()
  db.close()
