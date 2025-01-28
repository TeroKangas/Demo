import sqlite3



class LevelSystem:
    def __init__(self, db_path, user_id, max_level=80, xp_per_level=1000):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.user_id = user_id
        self.max_level = max_level
        self.xp_per_level = xp_per_level
        self.current_level, self.current_xp = self.load_user_data()

    def load_user_data(self):
        """Lädt das aktuelle Level und XP des Spielers aus der Datenbank."""
        self.cursor.execute("SELECT level, xp FROM user WHERE is_active = 1")
        result = self.cursor.fetchone()

        if result:
            print(f"Spieler-Daten geladen: Level {result[0]}, XP {result[1]}")
            return result[0], result[1]
        else:
            print("Spieler nicht gefunden, Standardwerte werden verwendet.")
            return 1, 0  # Standardwerte: Level 1, 0 XP

    def save_user_data(self):
        """Speichert das aktuelle Level und XP des Spielers in der Datenbank."""
        self.cursor.execute("UPDATE user SET level = ?, xp = ? WHERE is_active = 1",
                            (self.current_level, self.current_xp))
        self.conn.commit()
        print(f"Daten gespeichert: Level {self.current_level}, XP {self.current_xp}")

    def add_xp(self, xp):
        if self.current_level < self.max_level:
            self.current_xp += xp
            print(f"XP hinzugefügt: {xp}. Gesamt XP: {self.current_xp}")
            self.check_level_up()
        else:
            print("Maximales Level erreicht!")
        self.save_user_data()

    def check_level_up(self):
        while self.current_xp >= self.xp_per_level and self.current_level < self.max_level:
            self.current_xp -= self.xp_per_level
            self.current_level += 1
            print(f"Level aufgestiegen! Aktuelles Level: {self.current_level}")

    def get_current_state(self):
        return f"Level: {self.current_level}, XP: {self.current_xp}/{self.xp_per_level}"

    def close_connection(self):
        """Schließt die Verbindung zur Datenbank."""
        self.conn.close()


# Beispielhafte Verwendung:
#db_path = 'game.db'
#user_id = 1

# Levelsystem mit Verbindung zur Datenbank starten
#user = LevelSystem(db_path, user_id)

# XP hinzufügen und speichern
#user.add_xp(2500)
#print(user.get_current_state())  # Gibt den aktuellen Status zurück

# Mehr XP hinzufügen
#user.add_xp(5000)
#print(user.get_current_state())

# Verbindung zur Datenbank schließen
#user.close_connection()
