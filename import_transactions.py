import re
import datetime
import hashlib
import sqlite3
import os
import glob
from ofxtools.Parser import OFXTree
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def get_imports_files():
    return sorted(glob.glob('imports/*.ofx'))

def get_transactions(filename):
    transactions = []

    parser = OFXTree()
    parser.parse(filename)
    raw_transactions = parser.findall('.//STMTTRN')

    for raw_transaction in raw_transactions:
        transaction = get_transaction(raw_transaction)
        transactions.append(transaction)
    
    return transactions

def get_transaction(raw_transaction):
    label = raw_transaction.find('NAME').text.strip()
    amount = raw_transaction.find('TRNAMT').text.strip()
    raw_date = raw_transaction.find('DTPOSTED').text.strip()
    hash = hashlib.md5(label.encode('utf-8') + raw_date.encode('utf-8') + amount.encode('utf-8')).hexdigest()

    date = datetime.datetime.strptime(raw_date, "%Y%m%d")
    year = date.year
    month = date.month
    day = date.day
    
    return [year, month, day, label, float(amount.replace(',','.')), hash]

def insert_transactions(transactions):
    db = sqlite3.connect(DB_PATH)

    for transaction in transactions:
        year = transaction[0]
        month = transaction[1]
        day = transaction[2]
        label = transaction[3]
        amount = transaction[4]
        hash = transaction[5]

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO transactions ("year", "month", "day", label, amount, hash)
            SELECT ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS(SELECT 1 FROM transactions WHERE hash = ?);
            """, (year, month, day, label, amount, hash, hash))
        db.commit()
        cursor.close()
    db.close()

def archive_file(filename):
    os.rename(filename, "imports/archived/" + os.path.basename(filename))


#######################

print("\r\n##### IMPORTING TRANSACTIONS #####\r\n")

os.makedirs("imports/archived", exist_ok=True)

import_files = get_imports_files()

for import_file in import_files:
    print("Importing " + import_file)
    transactions = get_transactions(import_file)
    insert_transactions(transactions)
    archive_file(import_file)

print("\r\n##### TRANSACTIONS IMPORTED #####\r\n")