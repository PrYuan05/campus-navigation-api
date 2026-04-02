import sqlite3
import os

# Set up the path to the SQLite database file (we'll create it in the data folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "campus.db")

def init_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Create the locations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # 2. Create the paths table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_name TEXT NOT NULL,
            end_name TEXT NOT NULL,
            time_seconds INTEGER NOT NULL,
            FOREIGN KEY (start_name) REFERENCES locations (name),
            FOREIGN KEY (end_name) REFERENCES locations (name)
        )
    ''')

    # Clear old data (for convenient repeated testing)
    cursor.execute('DELETE FROM paths')
    cursor.execute('DELETE FROM locations')

    # 3. Prepare our initial location data
    locations = [
        "通訊系館_109", "通訊系館_110", "通訊系館_111", 
        "通訊系館_102", "通訊系館_走廊", "通訊系館_大門", 
        "教研大樓", "健雄館"
    ]
    
    for loc in locations:
        cursor.execute('INSERT INTO locations (name) VALUES (?)', (loc,))

    # 4. Prepare our initial path data (both directions)
    paths = [
        ("通訊系館_109", "通訊系館_走廊", 5),
        ("通訊系館_走廊", "通訊系館_109", 5),
        ("通訊系館_110", "通訊系館_走廊", 8),
        ("通訊系館_走廊", "通訊系館_110", 8),
        ("通訊系館_111", "通訊系館_走廊", 12),
        ("通訊系館_走廊", "通訊系館_111", 12),
        ("通訊系館_102", "通訊系館_走廊", 15),
        ("通訊系館_走廊", "通訊系館_102", 15),
        ("通訊系館_走廊", "通訊系館_大門", 20),
        ("通訊系館_大門", "通訊系館_走廊", 20),
        ("通訊系館_大門", "教研大樓", 180),
        ("教研大樓", "通訊系館_大門", 180),
        ("通訊系館_大門", "健雄館", 240),
        ("健雄館", "通訊系館_大門", 240),
        ("教研大樓", "健雄館", 120),
        ("健雄館", "教研大樓", 120)
    ]

    cursor.executemany('INSERT INTO paths (start_name, end_name, time_seconds) VALUES (?, ?, ?)', paths)

    # Save and close
    conn.commit()
    conn.close()
    print(f"✅ Database created successfully! Saved at: {DB_PATH}")

if __name__ == "__main__":
    init_db()