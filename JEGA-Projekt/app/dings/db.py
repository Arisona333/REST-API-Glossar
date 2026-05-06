import sqlite3
from datetime import datetime
import os

def init_db():
    create_table()

def get_all_begriffe():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Begriff")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_begriff_by_id(begriff_id):
    return get_begriff(begriff_id)

# Anpassung: create_begriff gibt jetzt das ganze Objekt zurück
def create_begriff_full(titel, beschreibung, kategorie_id=None):
    begriff_id = create_begriff(titel, beschreibung, kategorie_id)
    return get_begriff(begriff_id)

DB_PATH = "glossar_datenbank.db"
DB_FOLDER = "datenbank"
os.makedirs(DB_FOLDER, exist_ok=True)  # Ordner anlegen, falls er nicht existiert
DB_PATH = os.path.join(DB_FOLDER, "glossar_datenbank.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    
    #Users/ Autoren
    cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                role TEXT NOT NULL
)
""")
    #Kategorien
    cursor.execute("""CREATE TABLE IF NOT EXISTS Kategorie(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    beschreibung TEXT NOT NULL
)
""")

    #Begriffe
    cursor.execute("""CREATE TABLE IF NOT EXISTS Begriff(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titel TEXT NOT NULL,
                beschreibung TEXT NOT NULL,
                kategorie_id INTEGER,
                erstellt_am TEXT,
                aktualisiert_am TEXT,
                FOREIGN KEY (kategorie_id) REFERENCES Kategorie(id)
)
""")
       
    cursor.execute("""CREATE TABLE IF NOT EXISTS Begriff_History(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               user_id INTEGER NOT NULL,
               begriff_id INTEGER NOT NULL,
               aktion TEXT NOT NULL,
               datum TEXT NOT NULL,
               FOREIGN KEY (user_id) REFERENCES Users(id),
               FOREIGN KEY (begriff_id) REFERENCES Begriff(id)
               ) """) 
    
    conn.commit()
    conn.close()

# CREATE
def create_begriff(titel, beschreibung, kategorie_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    jetzt = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO Begriff (titel, beschreibung, kategorie_id, erstellt_am, aktualisiert_am)
        VALUES (?, ?, ?, ?, ?)
    """, (titel, beschreibung, kategorie_id, jetzt, jetzt))
    conn.commit()
    begriff_id = cursor.lastrowid
    conn.close()
    return begriff_id  

# READ
def get_begriff(begriff_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Begriff WHERE id=?", (begriff_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

# UPDATE
def update_begriff(begriff_id, titel=None, beschreibung=None, kategorie_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    jetzt = datetime.now().isoformat()
    updates = []
    werte = []
    if titel is not None:
        updates.append("titel=?")
        werte.append(titel)
    if beschreibung is not None:
        updates.append("beschreibung=?")
        werte.append(beschreibung)
    if kategorie_id is not None:
        updates.append("kategorie_id=?")
        werte.append(kategorie_id)
    if updates:
        updates.append("aktualisiert_am=?")
        werte.append(jetzt)
        sql = f"UPDATE Begriff SET {', '.join(updates)} WHERE id=?"
        werte.append(begriff_id)
        cursor.execute(sql, werte)
    conn.commit()
    conn.close()

# DELETE
def delete_begriff(begriff_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Begriff WHERE id=?", (begriff_id,))
    conn.commit()
    conn.close()

def get_begriffe_by_kategorie(kategorie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Begriff WHERE kategorie_id=?", (kategorie_id,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

#---------------------------------------------------#
# Funktionen für Kategorien

def get_all_kategorien():
    conn = get_connection() 
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Kategorie"
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_kategorien_by_id(kategorie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Kategorie WHERE id = ?", (kategorie_id,)
        )
    row = cursor.fetchone()
    conn.close
    if row:
        return dict(row)
    else:
        return None

def create_kategorie(name, beschreibung):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Kategorie (name, beschreibung) VALUES (?, ?)", (name, beschreibung)
    )
    conn.commit()
    kategorie_id = cursor.lastrowid
    conn.close()
    return get_kategorien_by_id(kategorie_id)

def update_kategorie(kategorie_id, name=None, beschreibung=None):
    conn = get_connection()
    cursor = conn.cursor()
    updates = []
    werte = []
    if name is not None:
        updates.append("name=?")
        werte.append(name)
    if beschreibung is not None:
        updates.append("beschreibung=?")
        werte.append(beschreibung)
    if updates:
        sql = f"UPDATE Kategorie SET {', '.join(updates)} WHERE id=?"
        werte.append(kategorie_id)
        cursor.execute(sql, werte)
    conn.commit()
    conn.close()

def delete_kategorie(kategorie_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Kategorie WHERE id = ?", (kategorie_id,))
    conn.commit()
    changes = cursor.rowcount  # Anzahl der gelöschten Zeilen
    conn.close()
    return changes > 0  # True = gelöscht, False = kein Treffer
#---------------------------------------------------#
# Funktionen für User

def get_all_users():
    conn = get_connection() 
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Users"
        )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM Users WHERE id = ?", (user_id,)
        )
    row = cursor.fetchone()
    conn.close
    if row:
        return dict(row)
    else:
        return None
    
def create_user(first_name, role):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Users (first_name, role) VALUES (?, ?)", (first_name, role)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return get_user_by_id(user_id)

def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE id = ?", (user_id,))
    conn.commit()
    changes = cursor.rowcount  # Anzahl der gelöschten Zeilen
    conn.close()
    return changes > 0  # True = gelöscht, False = kein Treffer


# Begriff-History Funktionen
def get_all_begriff_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Begriff_History")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def create_begriff_history(user_id, begriff_id, aktion):
    from datetime import datetime
    conn = get_connection()
    cursor = conn.cursor()
    datum = datetime.now().isoformat()
    cursor.execute(
        """
        INSERT INTO Begriff_History (user_id, begriff_id, aktion, datum)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, begriff_id, aktion, datum)
    )
    conn.commit()
    history_id = cursor.lastrowid
    conn.close()
    # Gib den neuen Eintrag zurück
    return get_begriff_history_by_id(history_id)

def get_begriff_history_by_id(history_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Begriff_History WHERE id=?", (history_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None