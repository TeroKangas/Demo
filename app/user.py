import sqlite3
from datetime import datetime


class UserManager:
    def __init__(self, db_path, user_id):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.user_id = user_id

    def createUser(self, name, image_path, race, clas, level, xp, is_active):
        """Erstellt einen neuen user"""
        self.cursor.execute('''
            INSERT INTO user (name, image_path, race, clas, level, xp, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, image_path, race, clas, level, xp, is_active))
        self.conn.commit()
        print(f"User '{name}' wurde erstellt.")
    
    def updateUser(self, id, name=None, image_path=None, race=None, clas=None):    
        set_clause = []
        params = []
        
        if name is not None:
            set_clause.append("name = ?")
            params.append(name)
        
        if image_path is not None:
            set_clause.append("image_path = ?")
            params.append(image_path)
        
        if race is not None:
            set_clause.append("race = ?")
            params.append(race)
        
        if clas is not None:
            set_clause.append("clas = ?")
            params.append(clas)

        if not set_clause:
            print(f"Keine Änderungen für User mit ID {id} vorgenommen.")
            return
        
        params.append(id)
        
        sql_query = f"UPDATE user SET {', '.join(set_clause)} WHERE id = ?"
        
        self.cursor.execute(sql_query, tuple(params))
        
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"User mit ID {id} wurde aktualisiert.")
        else:
            print(f"User mit ID {id} nicht gefunden oder keine Änderungen vorgenommen.")

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

    def activateUser(self, id: int):
        msg_string: str

        self.cursor.execute("UPDATE user SET is_active = 1 WHERE id = ?", (id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            msg_string = f"User ID{id} is active. "
        else:
            return (f"User activation failed.")

        self.cursor.execute("UPDATE user SET is_active = 0 WHERE id <> ?", (id,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            msg_string = msg_string + "Others than user ID{id} are inactivated."
        else:
            return(f"Users inactivation failed.")
        
        return msg_string
    
    def changePlayer(self, name: str):
        self.cursor.execute("UPDATE user SET is_active = 1 WHERE name = ?", (name,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
        else:
            return

        self.cursor.execute("UPDATE user SET is_active = 0 WHERE name <> ?", (name,))
        if self.cursor.rowcount > 0:
            self.conn.commit()
        else:
            return



