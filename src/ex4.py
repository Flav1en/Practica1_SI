import sqlite3
import pandas as pd
from datetime import datetime

def get_users_by_permission_type(permission_type: int):
    if permission_type not in [0, 1]:
        raise ValueError("The permission_type parameter must be either 0 or 1.")
    conn = sqlite3.connect('database.db')
    query = "SELECT * FROM users WHERE permissions=?"
    users_df = pd.read_sql_query(query, conn, params=(permission_type,))
    conn.close()
    return users_df

def get_dates_from_database():
    conn = sqlite3.connect('database.db')
    dates_df = pd.read_sql_query("SELECT * FROM dates", conn)
    conn.close()
    return dates_df

def calculate_average_date_difference(date_list):
    def get_date_difference(date1, date2):
        date_format = "%d/%m/%Y"
        try:
            datetime1 = datetime.strptime(date1, date_format)
            datetime2 = datetime.strptime(date2, date_format)
            return (datetime2 - datetime1).days
        except ValueError:
            raise ValueError("Invalid date format. Please use the format 'day/month/year'.")

    sorted_dates = sorted(date_list, key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
    differences = [get_date_difference(sorted_dates[i], sorted_dates[i+1]) for i in range(len(sorted_dates) - 1)]
    return round(sum(differences) / len(differences)) if differences else 0

def get_user_dates_dict(dates_df):
    user_dates_dict = {}
    for _, row in dates_df.iterrows():
        user_id = row['user_id']
        date = row['date']
        user_dates_dict.setdefault(user_id, []).append(date)
    return {user_id: calculate_average_date_difference(dates) for user_id, dates in user_dates_dict.items()}

def probability_of_phishing_emails():
    conn = sqlite3.connect('database.db')
    users = pd.read_sql_query("SELECT * FROM users", conn)
    users_prob = pd.DataFrame(columns=['id', 'probability'])
    for i, user in users.iterrows():
        if user['phishing_emails'] != 0:
            phishing_prob = user['clicked_emails'] / user['phishing_emails']
        else:
            phishing_prob = 0
        users_prob = users_prob._append({'id': user['id'], 'probability': phishing_prob}, ignore_index=True)
    return users_prob

def main():
    dates_df = get_dates_from_database()
    user_dates_dict = get_user_dates_dict(dates_df)

    admin_users_df = get_users_by_permission_type(1)
    normal_users_df = get_users_by_permission_type(0)

    admin_dates_df = pd.DataFrame({'id': admin_users_df['id'], 'date': admin_users_df['id'].map(user_dates_dict).fillna(0)})
    normal_dates_df = pd.DataFrame({'id': normal_users_df['id'], 'date': normal_users_df['id'].map(user_dates_dict).fillna(0)})

    admin_normal = admin_dates_df['date'].mean()
    average_normal = normal_dates_df['date'].mean()
    
    print(f"Average date difference for admin users: {admin_normal}")
    print(f"Average date difference for normal users: {average_normal}")
    
    print(f"Probability of phishing emails:", probability_of_phishing_emails())
    
if __name__ == "__main__":
    main()
