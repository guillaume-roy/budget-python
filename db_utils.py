import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def select(query, args=(), one=False):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute(query, args)
  r = [dict((cursor.description[i][0], value)
            for i, value in enumerate(row)) for row in cursor.fetchall()]
  cursor.close()
  db.close()
  return (r[0] if r else None) if one else r

def execute(query, args=()):
  db = sqlite3.connect(DB_PATH)
  cursor = db.cursor()
  cursor.execute(query, args)
  db.commit()
  cursor.close()
  db.close()
