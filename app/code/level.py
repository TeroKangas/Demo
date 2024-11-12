import sqlite3
# import os

# Datenbank verbinden
db_path = r"C:\Users\lucie\PycharmProjects\Demo\app\db\db\game.db"
# conn = sqlite3.connect(db_path)

# Absoluten Pfad zur Datenbank anzeigen
# absolute_path = os.path.abspath(db_path)
# print(f"Datenbank gespeichert unter: {absolute_path}")


class LevelSystem:
    def __init__(self, db_path, player_id, max_level=80, xp_per_level=1000):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.player_id = player_id
        self.max_level = max_level
        self.xp_per_level = xp_per_level
        self.current_level, self.current_xp = self.load_player_data()

    def load_player_data(self):
        """Lädt das aktuelle Level und XP des Spielers aus der Datenbank."""
        self.cursor.execute("SELECT level, xp FROM player WHERE id = ?", (self.player_id,))
        result = self.cursor.fetchone()

        if result:
            print(f"Spieler-Daten geladen: Level {result[0]}, XP {result[1]}")
            return result[0], result[1]
        else:
            print("Spieler nicht gefunden, Standardwerte werden verwendet.")
            return 1, 0  # Standardwerte: Level 1, 0 XP

    def save_player_data(self):
        """Speichert das aktuelle Level und XP des Spielers in der Datenbank."""
        self.cursor.execute("UPDATE player SET level = ?, xp = ? WHERE id = ?",
                            (self.current_level, self.current_xp, self.player_id))
        self.conn.commit()
        print(f"Daten gespeichert: Level {self.current_level}, XP {self.current_xp}")

    def add_xp(self, xp):
        if self.current_level < self.max_level:
            self.current_xp += xp
            print(f"XP hinzugefügt: {xp}. Gesamt XP: {self.current_xp}")
            self.check_level_up()
        else:
            print("Maximales Level erreicht!")
        self.save_player_data()

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
#player_id = 1

# Levelsystem mit Verbindung zur Datenbank starten
#player = LevelSystem(db_path, player_id)

# XP hinzufügen und speichern
#player.add_xp(2500)
#print(player.get_current_state())  # Gibt den aktuellen Status zurück

# Mehr XP hinzufügen
#player.add_xp(5000)
#print(player.get_current_state())

# Verbindung zur Datenbank schließen
#player.close_connection()
