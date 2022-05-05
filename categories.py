from db_utils import select, execute;

import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def create_category(label):
    execute("""
        INSERT INTO categories (label)
        VALUES (?);
        """, (label,))

def get_categories():
    return select("""
        SELECT id, label
        FROM categories
        ORDER BY label;
        """)

def delete_category(category_id):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("PRAGMA foreign_keys = ON;")
  cursor.execute("""
    DELETE FROM categories
    WHERE id = ?;
    """, (category_id,))
  db.commit()
  cursor.close()
  db.close()
