import sqlite3
from werkzeug.security import generate_password_hash

def add_user_with_role(database_path, username, email, password, first_name, last_name, is_active, is_admin, role_name):
    # Passwort hashen
    password_hash = generate_password_hash(password)

    # Verbindung zur Datenbank herstellen
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Rolle einfügen oder vorhandene Rolle finden
    cursor.execute("SELECT id FROM role WHERE name = ?", (role_name,))
    role = cursor.fetchone()
    if role is None:
        cursor.execute("INSERT INTO role (name) VALUES (?)", (role_name,))
        conn.commit()
        role_id = cursor.lastrowid
    else:
        role_id = role[0]

    # Neuen Nutzer einfügen
    cursor.execute("""
    INSERT INTO user (username, email, password_hash, first_name, last_name, is_active, is_admin)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (username, email, password_hash, first_name, last_name, is_active, is_admin))
    conn.commit()
    user_id = cursor.lastrowid

    # Verknüpfung zwischen Nutzer und Rolle einfügen
    cursor.execute("INSERT INTO user_role (user_id, role_id) VALUES (?, ?)", (user_id, role_id))
    conn.commit()

    # Verbindung schließen
    conn.close()
    print(f"Nutzer {username} mit der Rolle {role_name} wurde erfolgreich hinzugefügt.")

# Pfad zur Datenbankdatei
database_path = "C:\\Users\\Hendrik\\Documents\\Github\\Trainex aber besser\\database\\educampus.db"

# Nutzerdaten und Rolle erhalten
username = input("Benutzername: ")
email = input("E-Mail: ")
password = input("Passwort: ")
first_name = input("Vorname: ")
last_name = input("Nachname: ")
is_active = input("Ist der Benutzer aktiv? (j/n): ") == 'j'
is_admin = input("Ist der Benutzer ein Admin? (j/n): ") == 'j'
role_name = input("Rollenname: ")

# Funktion aufrufen
add_user_with_role(database_path, username, email, password, first_name, last_name, is_active, is_admin, role_name)
