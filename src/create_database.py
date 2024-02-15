import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

#creation of database tables
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        phone TEXT,
        password_hash TEXT,
        province TEXT,
        permissions INTEGER,
        total_emails INTEGER,
        phishing_emails INTEGER,
        clicked_emails INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dates (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        date TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ips (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        ip TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
''')


conn.commit()
conn.close()
