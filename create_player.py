from nicegui import ui
import sqlite3
import datetime

class Demo:

    def __init__(self):
        self.db_path = r"C:\Users\kanga\OneDrive\Työpöytä\Schule Bad Mergentheim\Sperl\nicegui\Demo\my_database.db"
        self.connection = sqlite3.connect(self.db_path)
        self.create_table()
        self.playerName = ''
        self.experience = 0
        self.level = 1
        self.race = ''
        self.players = self.fetch_all_players()
        
        # Create a container for the window's content
        self.content = ui.column()

    def create_table(self):
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS spieler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(200),
            beschreibung VARCHAR(200),
            erstellt DATETIME,
            bild BLOB,
            level INT,
            punkte INT
        );
        '''
        self.connection.execute(create_table_query)
        self.connection.commit()
    
    def insert_into_spieler(self):
        player_name = self.playerName
        race = self.race
        if self.check_if_name_already_exists(player_name):
            ui.notification(f"Player '{player_name}' already exists in the database!")
            return
        if len(player_name) > 10:
            ui.notification(f"Name length may not exceed 10 characters")
            return
        if player_name != "":
            insert_query = 'INSERT INTO spieler (name, level, punkte, rasse, erstellt) VALUES (?, ?, ?, ?, ?)'
            self.connection.execute(insert_query, (player_name, 1, 0, race, datetime.datetime.now()))
            self.connection.commit()
            self.players = self.fetch_all_players()  # Refresh the players list
            ui.notification(f"Player '{player_name}' created in the database!")

            self.clear_window()
            refresh_ui()

    def check_if_name_already_exists(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM spieler WHERE name = ?", (name,))
        count = cursor.fetchone()[0]
        return count > 0

    def fetch_all_players(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM spieler")
        return cursor.fetchall()

    def clear_window(self):
        self.content.clear()

demo = Demo()

def refresh_ui():
    with demo.content:
        
        # Use ui.row() to align elements next to each other (horizontally)
        with ui.row().style('align-items: center; justify-content: space-between; padding: 20px;'):
            
            # Add the image
            ui.image('C:\\Users\\kanga\\OneDrive\\Työpöytä\\dgw2g1kr.png').classes('rounded-lg').style('width: 150px; height: 150px;')
            
            # Add button to change picture
            ui.button("Add picture")

            # Label and input for name
        with ui.row().style('align-items: center; justify-content: space-between; padding: 20px;'):
                ui.label('Name:')
                ui.input(on_change=lambda e: setattr(demo, 'playerName', e.value))

            # Label and dropdown for race
        with ui.row().style('align-items: center; justify-content: space-between; padding: 20px;'):
            ui.label('Race:')
            ui.select(
                options={'Human': 'Human', 'Elf': 'Elf', 'Orc': 'Orc'},
                on_change=lambda e: setattr(demo, 'race', e.value)
            )
                
        with ui.row().style('align-items: center; justify-content: space-between; padding: 20px;'):
            # Add button to create a player
            ui.button('Create player', on_click=demo.insert_into_spieler)
      
refresh_ui()
ui.run()

