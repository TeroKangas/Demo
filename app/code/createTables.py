import sqlite3
import os

def create_tables_if_needed():

    db_dir = 'db'
    db_path = os.path.join(db_dir, 'game.db')

    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            name TEXT NOT NULL,
            image_path TEXT,
            picture_id INTEGER,
            race TEXT DEFAULT noRace,  --'Human', 'Elf', 'Gnome'
            clas TEXT DEFAULT noClass, -- 'Knight', 'Healer', 'Fighter'
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 0
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quest (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            difficulty TEXT NOT NULL,        -- Easy = 2; Normal = 5; Hard = 10
            start_date datetime NOT NULL,
            due_date datetime NOT NULL,       -- Datum als Text im Format DD-MM-YYYY
            status TEXT NOT NULL,         -- Status: 'open' oder 'completed'
            FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
        )  
    ''')

    conn.commit()
    conn.close()