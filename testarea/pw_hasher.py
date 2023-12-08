import sqlite3
from werkzeug.security import generate_password_hash

# Function to add a user and assign a role in the database
def add_user_and_role(database_path, username, password, email, role_name, is_active=True, is_admin=False):
    # Hash the password
    password_hash = generate_password_hash(password)
    
    # Establish a database connection
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    # Insert the new role if it does not exist
    cur.execute("SELECT id FROM role WHERE name = ?", (role_name,))
    role = cur.fetchone()
    if role is None:
        cur.execute("INSERT INTO role (name) VALUES (?)", (role_name,))
        role_id = cur.lastrowid
    else:
        role_id = role[0]

    # Insert a new user
    cur.execute("""
        INSERT INTO user (username, password_hash, email, is_active, is_admin) 
        VALUES (?, ?, ?, ?, ?)
    """, (username, password_hash, email, is_active, is_admin))
    user_id = cur.lastrowid

    # Assign the role to the user
    cur.execute("INSERT INTO user_role (user_id, role_id) VALUES (?, ?)", (user_id, role_id))

    # Commit the insertion
    conn.commit()
    print(f"User {username} with role {role_name} has been added to the database with email {email}.")

    # Close the connection
    conn.close()

# Replace with the path to your database file
database_path = 'C:\\Users\\Hendrik\\Documents\\Github\\Trainex aber besser\\database\\users.db'

# Input username, password, email, and role
username = input("Enter the username: ")
password = input("Enter the password: ")
email = input("Enter the email: ")
role_name = input("Enter the role name: ")
is_active_input = input("Is the user active? (y/n): ")
is_admin_input = input("Is the user an admin? (y/n): ")

# Convert is_active and is_admin to boolean
is_active = True if is_active_input.lower() == 'y' else False
is_admin = True if is_admin_input.lower() == 'y' else False

# Call the function with the user input
add_user_and_role(database_path, username, password, email, role_name, is_active, is_admin)
