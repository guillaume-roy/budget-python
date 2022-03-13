import re
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_categories_patterns():
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    SELECT cp.id, cp.pattern, cp.category_id, c.label AS category_label
    FROM category_patterns cp
    LEFT OUTER JOIN categories c ON cp.category_id = c.id
    """)
  categories = cursor.fetchall()
  cursor.close()
  db.close()
  return categories

def create_pattern(pattern, category):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    INSERT INTO category_patterns (pattern, category_id)
    VALUES (?, ?);
    """, (pattern,category,))
  db.commit()
  cursor.close()
  db.close()

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
