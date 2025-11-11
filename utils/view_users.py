import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'users.db')

def view_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, full_name, role, department FROM users')
    users = cursor.fetchall()
    conn.close()
    print("Users in database:")
    for user in users:
        print(f"ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Role: {user[3]}, Department: {user[4]}")

if __name__ == "__main__":
    view_users()
