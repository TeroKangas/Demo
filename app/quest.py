import sqlite3
from datetime import datetime
import user


class QuestManager:
    def __init__(self, db_path, user_id):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.user_id = user_id
        self.user_manager = user.UserManager(db_path, 1)

    def createQuest(self, name, description, difficulty, start_date, due_date):
        currUserId = self.user_manager.get_active_user_id()
        self.cursor.execute('''
            INSERT INTO quest (user_id, name, description, difficulty, start_date, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (currUserId, name, description, difficulty, start_date, due_date, 'open'))
        self.conn.commit()
        print(f"Quest '{name}' wurde erstellt.")

    def getAllQuests(self):
        self.cursor.execute("SELECT * FROM quest WHERE user_id = ?", (self.user_id,))
        quests = self.cursor.fetchall()
        print(f"{len(quests)} Quests gefunden.")
        return quests

    def getCompletedQuests(self):
        self.cursor.execute('''
            SELECT quest.* 
            FROM quest
            JOIN user
            ON quest.user_id = user.id
            WHERE quest.status = 'completed' AND user.is_active = 1; ''')
        completed_quests = self.cursor.fetchall()
        print(f"{len(completed_quests)} completed Quests found.")
        return completed_quests

    def getOpenQuests(self):
        self.cursor.execute('''
            SELECT quest.* 
            FROM quest
            JOIN user
            ON quest.user_id = user.id
            WHERE quest.status = 'open' AND user.is_active = 1; ''')
        open_quests = self.cursor.fetchall()
        print(f"{len(open_quests)} open Quests found.")
        return open_quests

    def completeQuest(self, quest_id):
        currUserId = self.user_manager.get_active_user_id()
        self.cursor.execute('''
            UPDATE quest SET status = 'completed' WHERE id = ? AND user_id = ?
        ''', (quest_id, currUserId))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"Quest mit ID {quest_id} abgeschlossen.")
        else:
            print(f"Quest mit ID {quest_id} nicht gefunden oder nicht berechtigt.")

    def deleteQuest(self, quest_id):
        currUserId = self.user_manager.get_active_user_id()
        self.cursor.execute("DELETE FROM quest WHERE id = ? AND user_id = ?", (quest_id, currUserId))
        if self.cursor.rowcount > 0:
            self.conn.commit()
            print(f"Quest mit ID {quest_id} wurde gelöscht.")
        else:
            print(f"Quest mit ID {quest_id} nicht gefunden oder nicht berechtigt.")

    def overdueQuests(self):
        currUserId = self.user_manager.get_active_user_id()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('''
            SELECT * FROM quest
            WHERE user_id = ? AND status = 'open' AND due_date < ?
        ''', (currUserId, current_date))
        overdue = self.cursor.fetchall()
        print(f"{len(overdue)} überfällige Quests gefunden.")
        return overdue

    def editQuest(self, quest_id = None, name = None, description = None, difficulty = None, start_date = None, due_date = None):
        currUserId = self.user_manager.get_active_user_id()
        self.cursor.execute('''
            UPDATE quest
            SET user_id = ?, name = ?, description = ?, difficulty = ?, start_date = ?, due_date = ?, status = ?
            WHERE id = ?;    
        ''', (currUserId, name, description, difficulty, start_date, due_date, 'open', quest_id))

        self.conn.commit()
        print(f"Quest '{name}' wurde edited.")


    def getHowMuchXp(self, id):
        self.cursor.execute('''
            SELECT difficulty 
            FROM quest 
            WHERE id = ?;
        ''', (id,)
            )
        result = self.cursor.fetchone()
        if result:
            if result[0] == "Easy":
                return 2

            elif result[0] == "Normal":
                return 5

            elif result[0] == "Hard":
                return 10

            else:
                return None
        else:
            return None

    def closeConnection(self):
        self.conn.close()