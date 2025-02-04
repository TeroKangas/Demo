import sqlite3
from nicegui import ui


class LevelSystem:
    def __init__(self, db_path, user_id, max_level=100, xp_per_level=15):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.user_id = user_id
        self.max_level = max_level
        self.xp_per_level = xp_per_level
        self.current_level, self.current_xp = self.load_user_data()

    def load_user_data(self):
        self.cursor.execute("SELECT level, xp FROM user WHERE is_active = 1")
        result = self.cursor.fetchone()

        if result:
            print(f"Spieler-Daten geladen: Level {result[0]}, XP {result[1]}")
            return result[0], result[1]
        else:
            print("Spieler nicht gefunden, Standardwerte werden verwendet.")
            return 1, 0  # Standardwerte: Level 1, 0 XP

    def save_user_data(self):
        self.cursor.execute("UPDATE user SET level = ?, xp = ? WHERE is_active = 1",
                            (self.current_level, self.current_xp))
        self.conn.commit()
        print(f"Daten gespeichert: Level {self.current_level}, XP {self.current_xp}")

    def add_xp(self, xp):
        result = self.load_user_data()
        self.current_level = result[0]
        checkLevelValue = result[0]
        self.current_xp = result[1]
        if self.current_level < self.max_level:
            self.current_xp += xp
            print(f"XP hinzugefügt: {xp}. Gesamt XP: {self.current_xp}")
            self.check_level_up()
            self.save_user_data()
            if checkLevelValue < self.current_level:
                ui.notify(f"Congratulations! You are now level {self.current_level}", type='positive')
        else:
            print("Maximales Level erreicht!")
            self.save_user_data()
            ui.notify(f"Congratulations! You hit the max level of 100!", type='positive')

    def check_level_up(self):
        while self.current_xp >= self.xp_per_level and self.current_level < self.max_level:
            self.current_xp -= self.xp_per_level
            self.current_level += 1
            print(f"Level aufgestiegen! Aktuelles Level: {self.current_level}")

    def get_current_state(self):
        return f"Level: {self.current_level}, XP: {self.current_xp}/{self.xp_per_level}"

    def close_connection(self):
        self.conn.close()