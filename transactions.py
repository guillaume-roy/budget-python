import re
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_transactions():
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute("""
    SELECT t.id, t."year", t."month", t."day", t.category_pattern_id, t.simulation_id, t.label, t.amount, t.hash, c.label AS category_label
    FROM transactions t
    LEFT OUTER JOIN category_patterns cp ON t.category_pattern_id = cp.id
    LEFT OUTER JOIN categories c ON cp.category_id = c.id
    ORDER BY t.year DESC, t.month DESC, t.day DESC;
    """)
  transactions = cursor.fetchall()
  cursor.close()
  db.close()
  return transactions
