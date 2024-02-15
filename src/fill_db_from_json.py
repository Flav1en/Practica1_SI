import json
import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

with open('../datos/users_data_online.json') as users_file:
    users_data = json.load(users_file)

for index, user in enumerate(users_data["usuarios"],start=1):
    for username, user_info in user.items():

        cursor.execute('''
            INSERT INTO users (username, phone, password_hash, province, permissions, total_emails, phishing_emails, clicked_emails)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (username, user_info['telefono'], user_info['contrasena'], user_info['provincia'],
            user_info['permisos'], user_info['emails']['total'], user_info['emails']['phishing'], user_info['emails']['cliclados']))

        for date in user_info['fechas']:
            cursor.execute('INSERT INTO dates (user_id, date) VALUES (?, ?)',
                        (index, date))

        for ip in user_info['ips']:
            cursor.execute('INSERT INTO ips (user_id, ip) VALUES (?, ?)',
                        (index, ip))


conn.commit()
