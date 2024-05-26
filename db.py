import sqlite3

db_lp = sqlite3.connect('storage.db')
cursor_db = db_lp.cursor()

sql_create = '''CREATE TABLE IF NOT EXISTS passwords(
                login TEXT PRIMARY KEY,
                password TEXT NOT NULL,
                movietype1 TEXT,
                movietype2 TEXT,
                movietype3 TEXT,
                booktype1 TEXT,
                booktype2 TEXT,
                booktype3 TEXT);'''

cursor_db.execute(sql_create)
db_lp.commit()

cursor_db.close()
db_lp.close()
