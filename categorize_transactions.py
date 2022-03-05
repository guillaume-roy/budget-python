import re
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_transactions(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, label
        FROM transactions
        WHERE category_id IS NULL
        """)
    transactions = cursor.fetchall()
    cursor.close()
    return transactions

def get_category_patterns(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT pattern, category_id
        FROM category_patterns
        """)
    patterns = cursor.fetchall()
    cursor.close()
    return patterns

def match_categories(transactions, patterns, db):
    cursor = db.cursor()
    for transaction in transactions:
        for pattern in patterns:
            match = re.search(str(pattern[0]), str(transaction[1]))
            if match != None:
                cursor.execute("UPDATE transactions SET category_id=? WHERE id=?",(pattern[1],transaction[0],))
    db.commit()
    cursor.close()
                

#######################

print("\r\n##### CATEGORIZING TRANSACTIONS #####\r\n")

db = sqlite3.connect(DB_PATH)

transactions = get_transactions(db)
patterns = get_category_patterns(db)
match_categories(transactions, patterns, db)

db.close()

print("\r\n##### TRANSACTIONS CATEGORIZED #####\r\n")