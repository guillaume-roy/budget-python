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
    SELECT id, "year", "month", "day", category_id, simulation_id, label, amount, hash
    FROM transactions;
    """)
  transactions = cursor.fetchall()
  cursor.close()
  db.close()
  return transactions
