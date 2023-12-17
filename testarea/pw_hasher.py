import sys
import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash

def create_connection():
    return psycopg2.connect(
        dbname="educampus",
        user="postgres",
        password="zoRRo123",
        host="localhost",
    )

def add_user(conn, username, email, password, first_name, last_name, is_active, is_admin):
    with conn.cursor() as cursor:
        password_hash = generate_password_hash(password)
        insert_query = sql.SQL("""
            INSERT INTO users (username, password_hash, email, first_name, last_name, is_active, is_admin)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """)

        cursor.execute(insert_query, (username, password_hash, email, first_name, last_name, is_active, is_admin))
        conn.commit()

def add_users_from_file(conn, file_path):
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
