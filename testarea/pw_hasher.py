import sys
import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash

def create_connection():
    """
    Creates a connection to the PostgreSQL database.

    Returns:
        conn (psycopg2.extensions.connection): The database connection object.
    """
    try:
        conn = psycopg2.connect(
            dbname="educampus",
            user="postgres",
            password="zoRRo123",
            host="localhost",
        )
        print("Connection established successfully.")
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def add_user(conn, username, email, password, first_name, last_name, is_active, is_admin):
    """
    Adds a user to the database.

    Args:
        conn (psycopg2.extensions.connection): The database connection object.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        is_active (bool): Indicates if the user is active.
        is_admin (bool): Indicates if the user is an admin.
    """
    try:
        if not all([username, email, password, first_name, last_name]):
            raise ValueError("Missing required fields")

        with conn.cursor() as cursor:
            password_hash = generate_password_hash(password)
            insert_query = sql.SQL("""
                INSERT INTO users (username, password_hash, email, first_name, last_name, is_active, is_admin)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """)

            cursor.execute(insert_query, (username, password_hash, email, first_name, last_name, is_active, is_admin))
            conn.commit()
            print("User added successfully.")
    except ValueError as ve:
        print(f"Invalid input: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")

def add_users_from_file(conn, file_path):
    """
    Adds users from a file to the database.

    Args:
        conn (psycopg2.extensions.connection): The database connection object.
        file_path (str): The path to the file containing user data.
    """
    print(f"Adding users from file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    username, email, password, first_name, last_name, is_active_str, is_admin_str = line.strip().split(',')
                    is_active = is_active_str.strip().lower() in ('true', 't', '1')
                    is_admin = is_admin_str.strip().lower() in ('true', 't', '1')
                    add_user(conn, username, email, password, first_name, last_name, is_active, is_admin)
                    print(f"Added user {username}")
                except ValueError:
                    print(f"Invalid data format in line: {line}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    The main function of the script.
    """
    conn = None
    try:
        conn = create_connection()
        if '-b' in sys.argv:
            bulk_file_path = sys.argv[sys.argv.index('-b') + 1]
            add_users_from_file(conn, bulk_file_path)
        else:
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            is_active = str(input("Is user active? (True/False): ").lower() in ('true', '1', 't'))
            is_admin = str(input("Is user admin? (True/False): ").lower() in ('true', '1', 't'))

            add_user(conn, username, email, password, first_name, last_name, is_active, is_admin)
            print("User added successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    main()
