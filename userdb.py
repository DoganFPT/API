import sqlite3

conn = sqlite3.connect("userdb.db")

cursor = conn.cursor()

cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')

conn.commit()
conn.close()

print("Succesfully created 'user database'")

