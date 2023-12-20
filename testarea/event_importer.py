import psycopg2
import sys

# Define your database configuration here
DB_CONFIG = {
    'dbname': 'educampus',
    'user': 'postgres',
    'password': 'zoRRo123',
    'host': 'localhost'
}

def create_connection(db_config):
    """
    Create a database connection using the provided configuration.

    :param db_config: A dictionary containing the DB connection parameters
    :return: A new database connection object
    """
    return psycopg2.connect(**db_config)

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
    """
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO event (title, event_type_id, start_time, end_time, description, room_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, event_type_id, start_time, end_time, description, room_id))
        conn.commit()

def bulk_add_events(conn, filepath):
    """
    Bulk add events to the database from a file.

    :param conn: The database connection object
    :param filepath: The path to the file containing the events data
    """
    with open(filepath, 'r') as file:
        for line in file:
            title, event_type_id, start_time, end_time, description, room_id = line.strip().split(',')
            add_event(conn, title, event_type_id, start_time, end_time, description, room_id)

def main():
    """
    The main function of the program.
    """
    conn = create_connection(DB_CONFIG)
    
    if '-b' in sys.argv:
        filepath = sys.argv[sys.argv.index('-b') + 1]
        bulk_add_events(conn, filepath)
    else:
        # Interactive mode for adding a single event
        title = input("Enter event title: ")
        event_type_id = input("Enter event type ID: ")
        start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
        end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
        description = input("Enter event description: ")
        room_id = input("Enter room ID: ")
        add_event(conn, title, event_type_id, start_time, end_time, description, room_id)
    
    conn.close()

if __name__ == "__main__":
    main()
