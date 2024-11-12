import sqlite3

class Database:
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

# Example usage
db = Database()
db.connection.close()
