import sqlite3
import pandas as pd
import hashlib
import sqlite3
import useful_functions as uf

users_weak_password = uf.get_users_with_weak_passwords()
users_strong_password = uf.get_users_with_strong_passwords()
users_admin = uf.get_users_by_permission_type(1)
users_non_admin = uf.get_users_by_permission_type(0)

for label, df in [("Weak Password Users", users_weak_password),
                  ("Strong Password Users", users_strong_password),
                  ("Admin Users", users_admin),
                  ("Non-Admin Users", users_non_admin)]:
    num_samples = df.shape[0]
    province_none_count = len(df[df['province'] == "None"])
    phone_none_count = len(df[df['phone'] == "None"])
    median_phishing_emails = df['phishing_emails'].median()
    avg_phishing_emails = df['phishing_emails'].mean()
    var_phishing_emails = df['phishing_emails'].var()
    min_phishing_emails = df['phishing_emails'].min()
    max_phishing_emails = df['phishing_emails'].max()
    
    print("\n\nData for:", label)
    print("Number of observations:", num_samples)
    print("Number of missing values (i.e None):", province_none_count + phone_none_count)
    print("Median of phishing emails:", median_phishing_emails)
    print("Average of phishing emails:", avg_phishing_emails)
    print("Variance of phishing emails:", var_phishing_emails)
    print("Min and max values of phishing emails:", min_phishing_emails, max_phishing_emails)
