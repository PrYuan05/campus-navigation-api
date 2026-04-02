from fastapi import APIRouter, Query, HTTPException
from app.services.dijkstra import find_shortest_path
from app.models.schemas import RouteResponse
import sqlite3
import os

# Create a router for the API endpoints related to navigation
router = APIRouter()

# Load the campus map from a JSON file. This allows us to easily update the map without changing the code.
# Here we use a relative path to locate data/campus_map.json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "campus.db")

# Helper function: Build Graph dictionary from database in real-time
def get_graph_from_db():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail="Database does not exist, please run init_db.py first")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Fetch all paths from database
    cursor.execute("SELECT start_name, end_name, time_seconds FROM paths")
    rows = cursor.fetchall()
    conn.close()
    
    # Convert database data into dictionary format that Dijkstra algorithm understands
    graph = {}
    for start, end, time in rows:
        if start not in graph:
            graph[start] = {}
        graph[start][end] = time
        
    return graph

@router.get("/route", response_model=RouteResponse)
def get_route(
    start: str = Query(..., description="Starting location"),
    end: str = Query(..., description="Destination location")
):
    # 1. Fetch the latest map from database on each request
    campus_map = get_graph_from_db()
    
    # 2. Check if locations exist
    if start not in campus_map or end not in campus_map:
        raise HTTPException(status_code=404, detail="Specified location not found")
        
    # 3. Call the original algorithm (no changes needed!)
    route, total_time = find_shortest_path(campus_map, start, end)
    
    if not route:
        raise HTTPException(status_code=400, detail="Cannot find route to destination")
    
    return {
        "status": "success",
        "start_point": start,
        "end_point": end,
        "path": route,
        "estimated_time_seconds": total_time
    }