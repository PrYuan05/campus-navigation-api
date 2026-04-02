import sqlite3
import os
import csv

# 設定檔案路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "campus.db")
CSV_PATH = os.path.join(BASE_DIR, "data", "buildings.csv")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Removing old tables...")
    cursor.execute('DROP TABLE IF EXISTS paths')
    cursor.execute('DROP TABLE IF EXISTS locations')

    print("Creating new tables...")
    # 1. Create locations table (with lat/lon columns)
    cursor.execute('''
        CREATE TABLE locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            lat REAL,
            lon REAL
        )
    ''')

    # 2. Create paths table (temporarily empty, will import routes later)
    cursor.execute('''
        CREATE TABLE paths (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_name TEXT NOT NULL,
            end_name TEXT NOT NULL,
            time_seconds INTEGER NOT NULL,
            FOREIGN KEY (start_name) REFERENCES locations (name),
            FOREIGN KEY (end_name) REFERENCES locations (name)
        )
    ''')

    # 3. Automatically read CSV and import data
    if os.path.exists(CSV_PATH):
        print(f"Found CSV file: {CSV_PATH}, preparing to import...")
        with open(CSV_PATH, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Convert each row in the CSV to (name, lat, lon) format
            locations_data = [(row['name'], float(row['lat']), float(row['lon'])) for row in reader]

        # Batch insert into the database
        cursor.executemany('INSERT INTO locations (name, lat, lon) VALUES (?, ?, ?)', locations_data)
        print(f"🎉 Successfully imported {len(locations_data)} campus landmarks!")
    else:
        print(f"⚠️ CSV file not found! Please make sure it is placed at {CSV_PATH}")

    # Commit and close
    conn.commit()
    conn.close()
    print(f"✅ Database rebuild complete! Your API now has real latitude and longitude data!")

if __name__ == "__main__":
    init_db()