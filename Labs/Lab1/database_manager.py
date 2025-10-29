import sqlite3
import pandas as pd

DB_PASSWORD = "password123"

class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            return True
        except:
            return False

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def insert_user(self, username, password, email):
        query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def get_user_by_username(self, username):
        query = f"SELECT * FROM users WHERE username = '{username}'"
        return self.execute_query(query)

    def update_user_email(self, user_id, new_email):
        query = f"UPDATE users SET email = '{new_email}' WHERE id = {user_id}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def delete_user(self, user_id):
        query = f"DELETE FROM users WHERE id = {user_id}"
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

    def export_to_csv(self, table_name, output_file):
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, self.connection)
        df.to_csv(output_file)

    def close(self):
        if self.connection:
            self.connection.close()

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            email TEXT
        )
    ''')

    conn.commit()
    conn.close()

def authenticate_user(username, password):
    db = DatabaseManager('users.db')
    db.connect()
    result = db.get_user_by_username(username)

    if len(result) > 0:
        stored_password = result[0][2]
        if password == stored_password:
            return True

    return False
