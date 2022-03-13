import sqlite3
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_NAME")

def check_migrations_table_exist(db):
    cursor = db.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='migrations'")
    result = cursor.fetchone()

    if result == None or result[0] == 0:
        cursor.execute("""
            CREATE TABLE migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL
            )""")

    cursor.close()

def get_migration_files():
    return sorted(os.listdir("migrations/"))

def is_migration_always_exists(path, db):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM migrations WHERE name = ?;", (str(path),))
    result = cursor.fetchone()
    if result != None and result[0] == 1:
        cursor.close()
        return True
    else:
        cursor.close()
        return False

def execute_migration_file(path, db):
    if is_migration_always_exists(path, db):
        return

    print("Execution of " + path)
    file = open("migrations/" + path, "r")
    cursor = db.cursor()
    cursor.executescript(file.read())
    cursor.execute("INSERT INTO migrations (name, date) VALUES(?, ?);",(str(path), str(datetime.datetime.now()),))
    db.commit()
    cursor.close()

##########################

print("\r\n##### EXECUTING MIGRATIONS #####\r\n")

db = sqlite3.connect(DB_PATH)

check_migrations_table_exist(db)

migrations = get_migration_files()

for migration in migrations:
    execute_migration_file(migration, db)

db.close()
print("\r\n##### MIGRATION EXECUTED #####\r\n")
