import sqlite3
import pandas as pd

conn = sqlite3.connect('database.db')

users_df = pd.read_sql_query("SELECT * FROM users", conn)
dates_df = pd.read_sql_query("SELECT * FROM dates", conn)
ips_df = pd.read_sql_query("SELECT * FROM ips", conn)

conn.close()

num_samples = users_df.shape[0]

avg_dates_modified = dates_df.groupby('user_id')['date'].count().mean()
std_dates_modified = dates_df.groupby('user_id')['date'].count().std()

avg_total_ips = ips_df.groupby('user_id')['ip'].count().mean()
std_total_ips = ips_df.groupby('user_id')['ip'].count().std()

avg_phishing_emails = users_df['phishing_emails'].mean()
std_phishing_emails = users_df['phishing_emails'].std()

min_total_emails = users_df['total_emails'].min()
max_total_emails = users_df['total_emails'].max()

admin_users_df = users_df[users_df['permissions'] == 1]  # because 1 is the code for admin
min_phishing_admin = admin_users_df['phishing_emails'].min()
max_phishing_admin = admin_users_df['phishing_emails'].max()


print("Number of samples:", num_samples)
print("Average and standard deviation of the number of total dates password modified:",
      avg_dates_modified, std_dates_modified)
print("Average and standard deviation of the total detected IPs:", avg_total_ips, std_total_ips)
print("Average and standard deviation of the number of phishing emails interacted with:",
      avg_phishing_emails, std_phishing_emails)
print("Min and max values of total received emails:", min_total_emails, max_total_emails)
print("Min and max values of phishing emails interacted with by an administrator:",
      min_phishing_admin, max_phishing_admin)
