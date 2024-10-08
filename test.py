from nicegui import ui
import sqlite3

class Demo:
    def __init__(self):
        self.db_path = r"C:\Users\kanga\OneDrive\Työpöytä\Schule Bad Mergentheim\Sperl\nicegui\Demo\my_database.db"
        self.connection = self.create_database_if_not_exists()
        self.create_table()

    def create_database_if_not_exists(self):
        # Connects to the database (creates it if it doesn't exist)
        return sqlite3.connect(self.db_path)

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
        print("Table 'spieler' created or already exists.")

    def check_if_name_already_exists(self, name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM spieler WHERE name = ?", (name,))
        count = cursor.fetchone()[0]
        return count > 0

    def insert_into_spieler(self):
        player_name = self.text  # Use the text attribute from input
        if self.check_if_name_already_exists(player_name):
            ui.notify(f"Player '{player_name}' exists already in the database!")
        else:
            insert_query = 'INSERT INTO spieler (name) VALUES (?)'
            self.connection.execute(insert_query, (player_name,))
            self.connection.commit()
            ui.notify(f"Player '{player_name}' created in the database!")

demo = Demo()

with ui.row():
    ui.label('Create Player:')
    ui.input(on_change=lambda e: setattr(demo, 'text', e.value))
    ui.button('Create player', on_click=demo.insert_into_spieler)

ui.run()
