import re
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def create_category(label):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    INSERT INTO categories (label)
    VALUES (?);
    """, (label,))
  db.commit()
  cursor.close()
  db.close()

def get_categories():
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    SELECT id, label
    FROM categories
    """)
  categories = cursor.fetchall()
  cursor.close()
  db.close()
  return categories

def delete_category(id):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    DELETE FROM categories
    WHERE id = ?;
    """, (id,))
  db.commit()
  cursor.close()
  db.close()
