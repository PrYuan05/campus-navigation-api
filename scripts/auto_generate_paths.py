import sqlite3
import os
import math
import csv

# Haversine Formula
# Set paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "campus.db")
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "paths.csv")

# Set algorithm parameters
MAX_DISTANCE_METERS = 150  # Only connect locations within 150 meters
WALKING_SPEED_MPS = 1.2    # Average walking speed is about 1.2 meters/second

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate the real-world distance between two latitude/longitude points (in meters)"""
    R = 6371000  # Earth's radius (meters)
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c

def generate_paths():
    if not os.path.exists(DB_PATH):
        print("Database not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, lat, lon FROM locations")
    locations = cursor.fetchall()
    conn.close()

    paths = []
    connection_count = 0

    print(f"Starting analysis of spatial topology for {len(locations)} locations...")

    # Compare all locations pairwise
    for i in range(len(locations)):
        for j in range(i + 1, len(locations)):
            loc1 = locations[i]
            loc2 = locations[j]
            
            # Calculate distance
            dist = haversine_distance(loc1[1], loc1[2], loc2[1], loc2[2])
            
            # If the distance is less than our threshold, automatically create a connection
            if dist <= MAX_DISTANCE_METERS:
                time_seconds = int(dist / WALKING_SPEED_MPS)
                
                # To avoid very short times (e.g., less than 1 second for 1 meter), set a minimum limit
                if time_seconds < 10:
                    time_seconds = 10
                
                # Write bidirectional paths
                paths.append([loc1[0], loc2[0], time_seconds])
                paths.append([loc2[0], loc1[0], time_seconds])
                connection_count += 1

    # Output to CSV for preview and manual adjustment
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["start_name", "end_name", "time_seconds"])
        writer.writerows(paths)

    print(f"🎉 Algorithm execution complete!")
    print(f"Successfully generated {connection_count * 2} navigation paths within {MAX_DISTANCE_METERS} meters!")
    print(f"Results have been saved to {OUTPUT_CSV}, you can run init_db.py to import them into the database.")

if __name__ == "__main__":
    generate_paths()