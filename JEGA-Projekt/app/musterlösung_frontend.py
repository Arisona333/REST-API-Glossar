import requests
import json

#API_URL = "http://127.0.0.1:8000" #<-- Wenn ihr Uvicorn über euren PC startet
API_URL = "http://192.168.1.100:8000" #<-- Wenn ihr Uvicorn über den Server Startet

# Hilfsfunktion für schöne Ausgabe
def pretty_print(response):
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

# 1. Alle Begriffe abrufen
def get_all_begriffe():
    r = requests.get(f"{API_URL}/begriffe/")
    pretty_print(r)

# 2. Einzelnen Begriff abrufen
def get_begriff(begriff_id):
    r = requests.get(f"{API_URL}/begriffe/{begriff_id}")
    pretty_print(r)

# 3. Begriff anlegen
def create_begriff(titel, beschreibung, kategorie_id, user_id):
    payload = {
        "titel": titel,
        "beschreibung": beschreibung,
        "kategorie_id": kategorie_id
    }
    r = requests.post(f"{API_URL}/begriffe/?user_id={user_id}", json=payload)
    pretty_print(r)

# 4. Begriff bearbeiten W.I.P.
def update_begriff(begriff_id, titel, beschreibung, kategorie_id, user_id):
    payload = {
        "titel": titel,
        "beschreibung": beschreibung,
        "kategorie_id": kategorie_id
    }
    r = requests.put(f"{API_URL}/begriffe/{begriff_id}?user_id={user_id}", json=payload)
    pretty_print(r)

# 5. Begriff löschen (nur Ausbilder) W.I.P.
def delete_begriff(begriff_id, user_id):
    r = requests.delete(f"{API_URL}/begriffe/{begriff_id}?user_id={user_id}")
    pretty_print(r)

# 6. Alle Kategorien abrufen
def get_all_kategorien():
    r = requests.get(f"{API_URL}/kategorie/")
    pretty_print(r)

# 7. Kategorie anlegen W.I.P.
def create_kategorie(name, beschreibung):
    payload = {
        "name": name,
        "beschreibung": beschreibung
    }
    r = requests.post(f"{API_URL}/kategorien/", json=payload)
    pretty_print(r)

# 8. Alle User abrufen
def get_all_users():
    r = requests.get(f"{API_URL}/users/")
    pretty_print(r)

# 9. User anlegen
def create_user(first_name, role):
    payload = {
        "first_name": first_name,
        "role": role
    }
    r = requests.post(f"{API_URL}/users/", json=payload)
    pretty_print(r)

# 10. History abrufen
def get_history():
    r = requests.get(f"{API_URL}/begriff-history/")
    pretty_print(r)

if __name__ == "__main__":
    print("--- API Musterlösung Frontend ---")
    # Beispielaufrufe:
    # get_all_begriffe()
    # create_begriff("API", "Application Programming Interface", 1 , 2)
    # update_begriff(1, "API", "Schnittstelle für Programme", 1, 2)
    # delete_begriff(1, 1)
    # get_all_kategorien()
    # create_kategorie("Programmierung", "Begriffe zur Softwareentwicklung")
    # get_all_users()
    # create_user("Jens", "Ausbilder")
    # get_history()
    print("Bitte gewünschte Funktion im Code aktivieren!")
