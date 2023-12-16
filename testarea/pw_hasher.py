import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from werkzeug.security import generate_password_hash

# Replace these variables with your actual database connection info
db_name = "your_database_name"
db_user = "your_username"
db_password = "your_password"
db_host = "localhost"  # or your database server IP

# Connect to PostgreSQL
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Cursor to execute queries
cur = conn.cursor()

# Function to add user and assign a role in the database
def add_user_and_role(username, password, email, role_name, is_active=True, is_admin=False):
    # Hash the password
    password_hash = generate_password_hash(password)  # Replace with your actual hash function
    
    try:
        # Insert the new role if it does not exist
        cur.execute("SELECT id FROM role WHERE name = %s", (role_name,))
        role = cur.fetchone()
        if role is None:
            cur.execute("INSERT INTO role (name) VALUES (%s) RETURNING id", (role_name,))
            role_id = cur.fetchone()[0]
        else:
            role_id = role[0]

        # Insert a new user
        cur.execute("""
            INSERT INTO users (username, password_hash, email, is_active, is_admin) 
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """, (username, password_hash, email, is_active, is_admin))
        user_id = cur.fetchone()[0]

        # Assign the role to the user
        cur.execute("INSERT INTO user_role (user_id, role_id) VALUES (%s, %s)", (user_id, role_id))

        # Commit the transaction
        conn.commit()
        print(f"User {username} with role {role_name} has been added to the database with email {email}.")

    except Exception as e:
        # If any error occurs, rollback the transaction
        conn.rollback()
        print(f"An error occurred: {e}")

    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()

def create_password_hash(password):
    """
    Generate a password hash using werkzeug's security module.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: A password hash.
    """
    # The method='bcrypt' parameter defines the hash method to use.
    password_hash = generate_password_hash(password, method='bcrypt')
    return password_hash

# Example usage
if __name__ == "__main__":
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
    add_user_and_role(username, password, email, role_name, is_active, is_admin)
