import sqlite3
from datetime import datetime


class QuestManager:
    def __init__(self, db_path, user_id):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.user_id = user_id

    def createQuest(self, name, description, difficulty, start_date, due_date):
        """Erstellt eine neue Quest für den Benutzer."""
        self.cursor.execute('''
            INSERT INTO quest (user_id, name, description, difficulty, start_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (self.user_id, name, description, difficulty, start_date, due_date, 'open'))
        self.conn.commit()
        print(f"Quest '{name}' wurde erstellt.")

    def getAllQuests(self):
        """Ruft alle Quests des Benutzers ab."""
        self.cursor.execute("SELECT * FROM quest WHERE user_id = ?", (self.user_id,))
        quests = self.cursor.fetchall()
        print(f"{len(quests)} Quests gefunden.")
        return quests

    def getOpenQuests(self):
        """Ruft alle offenen Quests des Benutzers ab."""
        self.cursor.execute("SELECT * FROM quest WHERE user_id = ? AND status = 'open'", (self.user_id,))
        open_quests = self.cursor.fetchall()
        print(f"{len(open_quests)} offene Quests gefunden.")
        return open_quests

    def completeQuest(self, quest_id):
        """Markiert eine Quest als abgeschlossen."""
        self.cursor.execute('''
            UPDATE quest SET status = 'completed' WHERE id = ? AND user_id = ?
        ''', (quest_id, self.user_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"Quest mit ID {quest_id} abgeschlossen.")
        else:
            print(f"Quest mit ID {quest_id} nicht gefunden oder nicht berechtigt.")

    def deleteQuest(self, quest_id):
        """Löscht eine Quest aus der Datenbank."""
        self.cursor.execute("DELETE FROM quest WHERE id = ? AND user_id = ?", (quest_id, self.user_id))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"Quest mit ID {quest_id} wurde gelöscht.")
        else:
            print(f"Quest mit ID {quest_id} nicht gefunden oder nicht berechtigt.")

    def overdueQuests(self):
        """Ruft alle überfälligen Quests ab."""
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            SELECT * FROM quest
            WHERE user_id = ? AND status = 'open' AND due_date < ?
        ''', (self.user_id, current_date))
        overdue = self.cursor.fetchall()
        print(f"{len(overdue)} überfällige Quests gefunden.")
        return overdue
    
    def editQuest(self, quest_id = None, name = None, description = None, difficulty = None, start_date = None, due_date = None):
        """Bearbeitet eine bestehende Quest."""

        self.cursor.execute('''
            UPDATE quest
            SET user_id = ?, name = ?, description = ?, difficulty = ?, start_date = ?, due_date = ?, status = ?
            WHERE id = ?;    
        ''', (1, name, description, difficulty, start_date, due_date, 'open', quest_id))

        self.conn.commit()
        print(f"Quest '{name}' wurde edited.")

    def closeonnection(self):
        """Schließt die Verbindung zur Datenbank."""
        self.conn.close()
