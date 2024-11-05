from nicegui import ui
import sqlite3
import hashlib

class Demo:

    def __init__(self):
        self.db_path = r"C:\Users\kanga\OneDrive\Työpöytä\Schule Bad Mergentheim\Sperl\nicegui\Demo\my_database.db"
        self.connection = sqlite3.connect(self.db_path)
        self.text = ''
        self.players = self.fetch_all_players()
        self.content = ui.column()

    def fetch_all_players(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, name FROM spieler")
        return cursor.fetchall()

    def update_player_name(self, player_id, new_name):
        update_query = 'UPDATE spieler SET name = ? WHERE id = ?'
        self.connection.execute(update_query, (new_name, player_id))
        self.connection.commit()
        self.players = self.fetch_all_players()  # Refresh the players list
        ui.notification(f"Player ID '{player_id}' updated to '{new_name}'")

        self.clear_window()
        refresh_ui()

    def remove_from_spieler(self, player_id):
        ui.notification("Remove player now...")
        remove_query = 'DELETE FROM spieler WHERE id = ?'
        self.connection.execute(remove_query, (player_id,))  # Corrected parameter passing
        self.connection.commit()
        ui.notification("Removed! Fetching...")
        self.players = self.fetch_all_players()  # Refresh the players list
        ui.notification(f"Removed: player ID '{player_id}'")  # Corrected typo in string

        self.clear_window()
        refresh_ui() 

    def clear_window(self):
        self.content.clear()

demo = Demo()

def generate_unique_color(player_name):
    # Use a hash of the player's name to generate a color
    hash_value = hashlib.md5(player_name.encode()).hexdigest()
    r = int(hash_value[:2], 16)
    g = int(hash_value[2:4], 16)
    b = int(hash_value[4:6], 16)
    return f'#{r:02x}{g:02x}{b:02x}'  # Return color in hex format

def refresh_ui():
    with demo.content:
        ui.label('Player List:')
        for player in demo.players:
            player_id, player_name = player
            bg_color = generate_unique_color(player_name)  # Generate a unique color for each player

            # Create a container for each player with a unique background color
            with ui.column().style(f'background-color: {bg_color}; padding: 16px; border-radius: 8px; margin-bottom: 10px;'):
                ui.image('C:\\Users\\kanga\\OneDrive\\Työpöytä\\dgw2g1kr.png').classes('rounded-lg w-full')
                ui.input(value=player_name, on_change=lambda e, id=player_id: demo.update_player_name(id, e.value))
                ui.button('Use player')
                ui.button('See statistics')
                ui.button('Remove player', on_click=lambda id=player_id: demo.remove_from_spieler(id))

refresh_ui()
ui.run()

