import sqlite3
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import hashlib

def get_users_by_permission_type(permission_type: int):
    """
    Fetches users from the database based on their permission type.

    This function connects to a SQLite database, executes a SQL query to fetch users based on their permission type,
    and returns the result as a pandas DataFrame.

    Args:
        permission_type (int): The permission type of the users to fetch. Must be either 0 or 1.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched users.

    Raises:
        ValueError: If the permission_type parameter is not 0 or 1.
    """
    if permission_type not in [0, 1]:
        raise ValueError("The permission_type parameter must be either 0 or 1.")
    with sqlite3.connect('database.db') as conn:
        query = "SELECT * FROM users WHERE permissions=?"
        users_df = pd.read_sql_query(query, conn, params=(permission_type,))
    return users_df


def get_dates_from_database():
    """
    Fetches dates from the database.

    This function connects to a SQLite database, executes a SQL query to fetch all dates,
    and returns the result as a pandas DataFrame.

    Returns:
        pandas.DataFrame: A DataFrame containing the fetched dates.
    """
    conn = sqlite3.connect('database.db')
    dates_df = pd.read_sql_query("SELECT * FROM dates", conn)
    conn.close()
    return dates_df




def calculate_average_date_difference(date_list):
    date_format = "%d/%m/%Y"
    sorted_dates = sorted(date_list, key=lambda x: datetime.strptime(x, date_format))
    differences = [(datetime.strptime(sorted_dates[i+1], date_format) - datetime.strptime(sorted_dates[i], date_format)).days for i in range(len(sorted_dates) - 1)]
    return round(sum(differences) / len(differences)) if differences else 0


def get_user_dates_dict(dates_df):
    """
    Creates a dictionary of users and their corresponding date differences.

    This function groups the DataFrame by the 'user_id' column and applies the list function to the 'date' column.
    It then calculates the average date difference for each user and returns a dictionary where the keys are the user IDs
    and the values are the average date differences.

    Args:
        dates_df (pandas.DataFrame): A DataFrame containing the dates associated with each user.

    Returns:
        dict: A dictionary where the keys are the user IDs and the values are the average date differences.
    """
    user_dates_dict = dates_df.groupby('user_id')['date'].apply(list).to_dict()
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


def load_data(file_path):
    """
    Charger les données à partir d'un fichier JSON.

    Args:
    - file_path (str): Chemin d'accès du fichier JSON.

    Returns:
    - dict: Données chargées depuis le fichier JSON.
    """
    with open(file_path) as file:
        data = json.load(file)
    return data


def get_worst_sites(data, num_sites=5):
    """
    Returns the worst sites based on their legal compliance.

    This function sorts the sites in the 'legal' section of the data based on the sum of their non-compliant attributes.
    It then returns the specified number of worst sites.

    Args:
        data (dict): The data containing the site information.
        num_sites (int, optional): The number of worst sites to return. Defaults to 5.

    Returns:
        list: A list of the worst sites based on their legal compliance.
    """
    return sorted(data["legal"], key=lambda x: sum(value == 0 for value in list(x.values())[0]))[-num_sites:]


def plot_password_change_intervals(admin_interval, normal_interval):
    """
    Plots the average password change intervals for admin and normal users.

    Args:
        admin_interval (float): The average password change interval for admin users.
        normal_interval (float): The average password change interval for normal users.
    """
    labels = ['Admin', 'Normal']
    intervals = [admin_interval, normal_interval]

    plt.figure(figsize=(8, 6))
    plt.bar(labels, intervals, color=['blue', 'orange'])
    plt.xlabel('Tipo de usuario')
    plt.ylabel('Intervalo medio de cambio de contraseña')
    plt.title('Intervalo medio de cambio de contraseña para usuarios Admin y Normal')
    plt.show()

def get_sites_with_outdated_policies(data):
    """
    Returns a dictionary of sites and their outdated policies.

    Args:
        data (dict): The data containing the site information.

    Returns:
        dict: A dictionary where the keys are the site names and the values are dictionaries of outdated policies.
    """
    outdated_policies_count = {}
    for site_entry in data["legal"]:
        site_name, site_data = site_entry.popitem()
        outdated_policies_count[site_name] = {policy: value == 0 for policy, value in site_data.items() if
                                              policy in ['cookies', 'aviso', 'proteccion_de_datos']}
    return outdated_policies_count


def plot_sites_with_most_outdated_policies(data, num_sites=5):
    """
    Plots the top 5 sites with the most outdated policies.

    Args:
        data (dict): The data containing the site information.
        num_sites (int, optional): The number of sites to plot. Defaults to 5.
    """
    outdated_policies_count = get_sites_with_outdated_policies(data)
    sorted_sites = sorted(outdated_policies_count.items(), key=lambda x: sum(x[1].values()), reverse=True)
    worst_sites = sorted_sites[:num_sites]

    sites, policy_counts = zip(*worst_sites)
    cookies, avisos, proteccion_de_datos = zip(*[list(site_policy.values()) for site_policy in policy_counts])

    bar_width = 0.3
    r1 = np.arange(len(sites))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    plt.figure(figsize=(10, 6))
    plt.barh(r1, cookies, color='red', height=bar_width, edgecolor='grey', label='Cookies desactualizados')
    plt.barh(r2, avisos, color='green', height=bar_width, edgecolor='grey', label='Avisos desactualizados')
    plt.barh(r3, proteccion_de_datos, color='blue', height=bar_width, edgecolor='grey',
             label='Proteccion de Datos desactualizados')

    plt.ylabel('Nombre del sitio web')
    plt.xlabel('Número de políticas desactualizadas')
    plt.title('Top 5 sitios web con más políticas desactualizadas')
    plt.yticks([r + bar_width for r in range(len(cookies))], sites)
    plt.gca().invert_yaxis()
    plt.legend()

    plt.show()

def respects_policies(data):
    """
    Returns two lists of sites that respect and do not respect privacy policies.

    Args:
        data (dict): The data containing the site information.

    Returns:
        tuple: A tuple containing two lists. The first list contains the sites that respect privacy policies.
        The second list contains the sites that do not respect privacy policies.
    """
    respecting_sites = []
    non_respecting_sites = []
    for site_info in data['legal']:
        for site, info in site_info.items():
            if info["cookies"] == 1 and info["aviso"] == 1 and info["proteccion_de_datos"] == 1:

                respecting_sites.append(site_info)
            else:

                non_respecting_sites.append(site_info)

    return respecting_sites, non_respecting_sites

def group_by_creation_year(data):
    """
    Groups sites by their creation year.

    Args:
        data (list): A list of dictionaries where each dictionary represents a site.

    Returns:
        dict: A dictionary where the keys are the creation years and the values are lists of sites created in those years.
    """
    sites_by_year = {}
    for entry in data:
        for site, info in entry.items():
            year = info['creacion']
            if year not in sites_by_year:
                sites_by_year[year] = []
            sites_by_year[year].append(site)

    # Trier le dictionnaire par année
    sites_by_year = {year: sites for year, sites in sorted(sites_by_year.items(), key=lambda item: int(item[0]))}

    return sites_by_year

# Fonction pour afficher les données avec Matplotlib
def plot_data(sites_by_year):
    """
    Plots the number of sites by their creation year.

    Args:
        sites_by_year (dict): A dictionary where the keys are the creation years and the values are lists of sites created in those years.
    """
    years = list(sites_by_year.keys())
    years.sort()

    sites_counts = [len(sites_by_year[year]) for year in years]

    plt.figure(figsize=(10, 6))
    plt.bar(years, sites_counts, color='b')
    plt.xlabel('Year of Creation')
    plt.ylabel('Number of Sites')
    plt.title('Number of Sites by Year of Creation')
    plt.show()
# Fonction pour traiter les données et les regrouper par année de création
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

def get_users_with_weak_passwords_and_probability():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    weak_passwords = get_weak_passwords()
    weak_passwords_str = ','.join(['"{}"'.format(mdp) for mdp in weak_passwords])
    query = f"SELECT * FROM users WHERE password_hash IN ({weak_passwords_str})"
    users_df = pd.read_sql_query(query, conn)
    conn.close()

    users_df['probability'] = users_df['clicked_emails'] / users_df['phishing_emails']

    # Afficher les 10 pires utilisateurs
    users_df = users_df.nlargest(10, 'probability')
    return users_df
def main():
    # Charger les données à partir du fichier JSON
    data = load_data("../datos/legal_data_online.json")
    dates_df = get_dates_from_database()

    user_dates_dict = get_user_dates_dict(dates_df)

    admin_users_df = get_users_by_permission_type(1)
    normal_users_df = get_users_by_permission_type(0)

    admin_dates_df = pd.DataFrame(
        {'id': admin_users_df['id'], 'date': admin_users_df['id'].map(user_dates_dict).fillna(0)})
    normal_dates_df = pd.DataFrame(
        {'id': normal_users_df['id'], 'date': normal_users_df['id'].map(user_dates_dict).fillna(0)})

    admin_interval = admin_dates_df['date'].mean()
    normal_interval = normal_dates_df['date'].mean()

    # Créer un DataFrame avec les intervalles moyens de changement de mot de passe
    df = pd.DataFrame({'Tipo': ['Admin', 'Normal'],
                       'Intervalo medio de cambio de contraseña': [admin_interval, normal_interval]})

    print(df)

    # Afficher les intervalles moyens de changement de mot de passe sous forme de graphique
    plot_password_change_intervals(admin_interval, normal_interval)

    # Afficher les 10 utilisateurs les plus critiques sous forme de graphique
    phishing_probabilities = probability_of_phishing_emails()
    top_10_critical_users = phishing_probabilities.nlargest(10, 'probability')

    # Charger les données des utilisateurs
    conn = sqlite3.connect('database.db')
    users_df = pd.read_sql_query("SELECT * FROM users", conn)

    # Fusionner les DataFrames des utilisateurs avec les probabilités de phishing
    merged_df = pd.merge(users_df, phishing_probabilities, on='id', how='left')

    plot_sites_with_most_outdated_policies(data)



    # Données fournies
    data = load_data("../datos/legal_data_online.json")

    # Appel de la fonction avec les données fournies
    respect, non_respect =respects_policies(data)

    sites_by_year = group_by_creation_year(respect)

    print("Sites respecting privacy",sites_by_year)

    sites_by_year = group_by_creation_year(non_respect)

    print("Sites not respecting privacy",sites_by_year)

    print(get_users_with_weak_passwords_and_probability())
    # Afficher les données avec Matplotlib


if __name__ == "__main__":
    main()
