import re
import sqlite3
import os
from dotenv import load_dotenv
from db_utils import select;

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_transactions():
    return select("""
        SELECT id, label
        FROM transactions
        WHERE category_pattern_id IS NULL AND category_id IS NULL
        """)

def get_category_patterns():
    return select("""
        SELECT id, pattern
        FROM category_patterns
        """)

def match_categories(transactions, patterns):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    for transaction in transactions:
        for p in patterns:
            match = re.search(str(p["pattern"]), str(transaction["label"]))
            if match != None:
                cursor.execute("UPDATE transactions SET category_pattern_id=? WHERE id=?",(p["id"],transaction["id"],))
    db.commit()
    cursor.close()
    db.close()


#######################

def start_categorization():
    transactions = get_transactions()
    patterns = get_category_patterns()
    match_categories(transactions, patterns)
