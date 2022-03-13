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
        SELECT id, label
        FROM transactions
        WHERE category_pattern_id IS NULL
        """)
    transactions = cursor.fetchall()
    cursor.close()
    db.close()
    return transactions

def get_category_patterns():
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, pattern
        FROM category_patterns
        """)
    patterns = cursor.fetchall()
    cursor.close()
    db.close()
    return patterns

def match_categories(transactions, patterns):
    db = sqlite3.connect(DB_PATH)
    cursor = db.cursor()
    for transaction in transactions:
        for pattern in patterns:
            match = re.search(str(pattern[1]), str(transaction[1]))
            if match != None:
                cursor.execute("UPDATE transactions SET category_pattern_id=? WHERE id=?",(pattern[0],transaction[0],))
    db.commit()
    cursor.close()
    db.close()


#######################

def start_categorization():
    transactions = get_transactions()
    patterns = get_category_patterns()
    match_categories(transactions, patterns)
