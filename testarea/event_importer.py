import psycopg2
import sys

# Define your database configuration here
DB_CONFIG = {
    'dbname': 'educampus',
    'user': 'postgres',
    'password': 'zoRRo123',
    'host': 'localhost'
}

# Exit codes
EXIT_SUCCESS = 0
EXIT_INVALID_ARGUMENTS = 1
EXIT_FILE_NOT_FOUND = 2
EXIT_DATABASE_ERROR = 3

def create_connection(db_config):
    """
    Create a database connection using the provided configuration.

    :param db_config: A dictionary containing the DB connection parameters
    :return: A new database connection object
    """
    try:
        return psycopg2.connect(**db_config)
    except psycopg2.Error as e:
        print(f"Failed to connect to the database: {e}")
        return EXIT_DATABASE_ERROR

def add_event(conn, title, event_type_id, start_time, end_time, description, room_id):
    """
    Add a new event to the database.

    :param conn: The database connection object
    :param title: The title of the event
    :param event_type_id: The ID of the event type
    :param start_time: The start time of the event
    :param end_time: The end time of the event
    :param description: The description of the event
    :param room_id: The ID of the room where the event takes place
    :return: The exit code
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO event (title, event_type_id, start_time, end_time, description, room_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (title, event_type_id, start_time, end_time, description, room_id))
            conn.commit()
        return EXIT_SUCCESS
    except psycopg2.Error as e:
        print(f"Failed to add event to the database: {e}")
        return EXIT_DATABASE_ERROR

def bulk_add_events(conn, filepath):
    """
    Bulk add events to the database from a file.

    :param conn: The database connection object
    :param filepath: The path to the file containing the events data
    :return: The exit code
    """
    try:
        with open(filepath, 'r') as file:
            for line in file:
                title, event_type_id, start_time, end_time, description, room_id = line.strip().split(',')
                exit_code = add_event(conn, title, event_type_id, start_time, end_time, description, room_id)
                if exit_code != EXIT_SUCCESS:
                    return exit_code
        return EXIT_SUCCESS
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return EXIT_FILE_NOT_FOUND

def main():
    """
    The main function of the program.
    """
    conn = create_connection(DB_CONFIG)
    exit_code = EXIT_SUCCESS
    
    if '-b' in sys.argv:
        if len(sys.argv) < 3:
            print("Invalid arguments. Usage: python event_importer.py -b <filepath>")
            exit_code = EXIT_INVALID_ARGUMENTS
        else:
            filepath = sys.argv[sys.argv.index('-b') + 1]
            exit_code = bulk_add_events(conn, filepath)
    else:
        # Interactive mode for adding a single event
        title = input("Enter event title: ")
        event_type_id = input("Enter event type ID: ")
        start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
        end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
        description = input("Enter event description: ")
        room_id = input("Enter room ID: ")
        exit_code = add_event(conn, title, event_type_id, start_time, end_time, description, room_id)
    
    conn.close()
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
