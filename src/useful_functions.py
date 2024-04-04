import pandas as pd
import sqlite3
import hashlib
import os

def get_weak_passwords():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT DISTINCT password_hash FROM users')
    password_hashes = cursor.fetchall()
    hashed_passwords = [password_hash[0] for password_hash in password_hashes]
    weak_passwords = []

    with open("rockyou.txt", "r", encoding="latin-1") as dic_file:
        for mot in dic_file:
            mot = mot.strip()
            hachage_md5 = hashlib.md5(mot.encode()).hexdigest()
            if hachage_md5 in hashed_passwords and not hachage_md5 in weak_passwords:
                weak_passwords.append(hachage_md5)

    conn.close()
    return weak_passwords

def get_users_with_weak_passwords():
    conn = sqlite3.connect('database.db')
    weak_passwords = get_weak_passwords()
    weak_passwords_str = ','.join(['"{}"'.format(mdp) for mdp in weak_passwords])
    query = f"SELECT * FROM users WHERE password_hash IN ({weak_passwords_str})"
    users_df = pd.read_sql_query(query, conn)
    conn.close()
    return users_df

def get_users_with_strong_passwords():
    conn = sqlite3.connect('database.db')
    weak_passwords = get_weak_passwords()
    weak_passwords_str = ','.join(['"{}"'.format(mdp) for mdp in weak_passwords])

    query = f"SELECT * FROM users WHERE password_hash NOT IN ({weak_passwords_str})"
    users_df = pd.read_sql_query(query, conn)
    
    conn.close()
    return users_df



def get_users_by_permission_type(permission_type: int):
    if permission_type not in [0, 1]:
        raise ValueError("The permission_type parameter must be either 0 or 1.")
    conn = sqlite3.connect('database.db')
    query = "SELECT * FROM users WHERE permissions=?"
    users_df = pd.read_sql_query(query, conn, params=(permission_type,))
    conn.close()
    return users_df
