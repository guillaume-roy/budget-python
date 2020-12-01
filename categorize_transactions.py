import re
import sqlite3

DB_PATH = "db/budget.db"
# DB_PATH = "db/budget_dev.db"

def get_transactions(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE category_id IS NULL
        """)
    transactions = cursor.fetchall()
    cursor.close()
    return transactions

def get_category_patterns(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT *
        FROM category_patterns
        """)
    patterns = cursor.fetchall()
    cursor.close()
    return patterns

def match_categories(transactions, patterns, db):
    cursor = db.cursor()
    for transaction in transactions:
        for pattern in patterns:
            match = re.search(str(pattern[1]), str(transaction[4]))
            if match != None:
                cursor.execute("UPDATE transactions SET category_id=? WHERE id=?",(pattern[2],transaction[0],))
    db.commit()
    cursor.close()
                

#######################

db = sqlite3.connect(DB_PATH)

transactions = get_transactions(db)
patterns = get_category_patterns(db)
match_categories(transactions, patterns, db)

db.close()

print("Finished")