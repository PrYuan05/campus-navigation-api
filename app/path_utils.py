import sqlite3
import math
import os

DB_PATH = os.path.join("data", "campus.db")

def point_to_segment_dist(px, py, x1, y1, x2, y2):
    """Calculate distance from point (px,py) to segment (x1,y1)-(x2,y2) in degrees"""
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0 and dy == 0:
        return math.hypot(px - x1, py - y1)
    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))
    proj_x = x1 + t * dx
    proj_y = y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

def get_landmarks_along_route(raw_steps, exclude_names=None):
    """
    Given a list of Google Maps route steps with coordinates,
    find SQLite DB locations that are strictly near the segments.
    """
    if exclude_names is None:
        exclude_names = []
        
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name, latitude, longitude FROM locations")
        all_locations = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"[DB Error in path_utils] {e}")
        return []

    # Filter out empty or missing coordinates
    locations = [loc for loc in all_locations if loc[1] is not None and loc[2] is not None]
    
    found_landmarks = []
    threshold = 0.0003  # Roughly 30-35 meters in degrees
    
    for step in raw_steps:
        start_lat = step.get('start_lat')
        start_lng = step.get('start_lng')
        end_lat = step.get('end_lat')
        end_lng = step.get('end_lng')
        
        if not (start_lat and start_lng and end_lat and end_lng):
            continue
            
        for name, lat, lng in locations:
            if name in exclude_names or name in found_landmarks:
                continue
                
            dist = point_to_segment_dist(lat, lng, start_lat, start_lng, end_lat, end_lng)
            if dist < threshold:
                found_landmarks.append(name)
                
    # Limit to top 3 landmarks to avoid overwhelming the user
    return found_landmarks[:3]
