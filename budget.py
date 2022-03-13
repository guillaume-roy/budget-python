import re
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_by_month():
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    select t.year, t.month, c.label as category_label, SUM(t.amount) as total
    from transactions t
    LEFT OUTER JOIN category_patterns cp on t.category_pattern_id = cp.id
    LEFT OUTER JOIN categories c on cp.category_id = c.id
    GROUP BY t.year, t.month, c.label
    """)
  categories = cursor.fetchall()
  cursor.close()
  db.close()
  return categories
