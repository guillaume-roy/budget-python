from openpyxl import load_workbook
import re
import datetime
import hashlib
import sqlite3
import os

# DB_PATH = "db/budget.db"
DB_PATH = "db/budget_dev.db"

def get_transactions(filename):
    wb = load_workbook(filename = filename, read_only=True)
    sheet = wb["Sheet0"]

    transactions = []
    rowIndex = 11
    while True:
        transaction = get_transaction_for_line(sheet, rowIndex)

        if transaction == None:
            break

        transactions.append(transaction);
        rowIndex = rowIndex + 1
    wb.close()
    return transactions

def get_transaction_for_line(sheet, line):
    row = sheet["A" + str(line) : "D" + str(line)]

    if len(row) == 0:
        return None

    hashSource = "";
    result = []
    for x in row[0]:
        if x.value == None:
            hashSource = hashSource + "";
            result.append(None)
        else:
            value = re.sub("\s+", " ", str(x.value).replace("\n", " - "))
            hashSource = hashSource + value
            result.append(value);
    result.append(hashlib.md5(hashSource).hexdigest())
    return result

def insert_transactions(transactions):
    db = sqlite3.connect(DB_PATH)

    for transaction in transactions:
        date = datetime.datetime.strptime(transaction[0], "%d/%m/%Y")
        year = date.year
        month = date.month
        day = date.day
        label = transaction[1]
        debit = 0 if transaction[2] == None else float(transaction[2])
        credit = 0 if transaction[3] == None else float(transaction[3])
        hash = transaction[4]

        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO transactions ("year", "month", "day", label, debit, credit, hash)
            SELECT ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS(SELECT 1 FROM transactions WHERE hash = ?);
            """, (year, month, day, label, debit, credit, hash, hash))
        db.commit()
        cursor.close()
    db.close()


#######################

transactions = get_transactions("imports/data.xlsx")
insert_transactions(transactions)

print("Finished")