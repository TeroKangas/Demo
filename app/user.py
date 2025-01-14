import sqlite3
from datetime import datetime


class UserManager:
    def __init__(self, db_path, user_id):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.user_id = user_id

    def createUser(self, name, image_path, race, clas, level, xp):
        """Erstellt einen neuen user"""
        self.cursor.execute('''
            INSERT INTO user (name, image_path, race, clas, level, xp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, image_path, race, clas, level, xp))
        self.conn.commit()
        print(f"User '{name}' wurde erstellt.")

    def updateUser(self, id, name, image_path, race, clas):
        """Aktualisiert alle Felder eines Benutzers."""
        self.cursor.execute('''
            UPDATE user 
            SET name = ?, image_path = ?, race = ?, clas = ?
            WHERE id = ?
        ''', (name, image_path, race, clas, id))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"User mit ID {id} wurde aktualisiert.")
        else:
            print(f"User mit ID {id} nicht gefunden.")

    def getAllUser(self):
        """Ruft alle Benutzer ab."""
        self.cursor.execute("SELECT * FROM user;")
        user = self.cursor.fetchall()
        print(f"{len(user)} User gefunden.")
        return user

    def deleteUser(self, id):
        """Löscht einen User aus der Datenbank."""
        self.cursor.execute("DELETE FROM user WHERE id = ?", (id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"User mit ID {id} wurde gelöscht.")
        else:
            print(f"User mit ID {id} nicht gefunden oder ein sonstiger Fehler trat auf.")



