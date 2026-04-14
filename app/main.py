import socket
orig_getaddrinfo = socket.getaddrinfo

def filtered_getaddrinfo(*args, **kwargs):
    responses = orig_getaddrinfo(*args, **kwargs)
    return [res for res in responses if res[0] == socket.AF_INET]

socket.getaddrinfo = filtered_getaddrinfo

import os
import json
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Import your Google Maps service
from app.maps_service import get_travel_time 

load_dotenv()
app = FastAPI()

# ==========================================
# 🧠 Vertex AI Configuration
# ==========================================

# NOTE: Since you've run 'gcloud auth application-default login', 
# the SDK will automatically find your credentials.
PROJECT_ID = "campus-navigation-api"  
LOCATION = "us-central1"      # Taiwan region
GEMINI_MODEL = "gemini-2.5-flash" 

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    credentials=None
)

# Database path relative to project root
DB_PATH = os.path.join("data", "campus.db")

# ==========================================
# 📊 Database Logic (Optimized)
# ==========================================

def get_relevant_locations(user_input: str):
    """Filter database to reduce context tokens (avoids 429 errors)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM locations")
        all_names = [row[0] for row in cursor.fetchall()]
        conn.close()

        # Simple keyword matching to narrow down the list
        relevant = [name for name in all_names if any(char in user_input for char in name)]
        
        # Fallback to a small subset if no keyword match
        return relevant if relevant else all_names[:15]
    except Exception as e:
        print(f"[DB Error] {e}")
        return []

def get_location_coords(location_name: str):
    """Lookup coordinates from DB."""
    if not location_name: return None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # Fuzzy match for robust lookup
        cursor.execute("SELECT latitude, longitude FROM locations WHERE name LIKE ?", (f"%{location_name}%",))
        result = cursor.fetchone()
        conn.close()
        return f"{result[0]},{result[1]}" if result else None
    except Exception as e:
        print(f"[DB Error] {e}")
        return None

# ==========================================
# 🛠️ API Endpoints
# ==========================================

class ChatRequest(BaseModel):
    user_message: str

@app.get("/")
async def root():
    return {"message": "NCU Campus Navigator API (Vertex AI Mode) is running."}

@app.post("/api/v1/chat-navigation")
async def process_chat_navigation(request: ChatRequest):
    # 1. Narrow down building list to save tokens
    relevant_list = get_relevant_locations(request.user_message)
    context_str = ", ".join(relevant_list)

    # 2. Build the NLU Prompt
    prompt = f"""
    You are a campus navigation expert. 
    Extract 'origin' and 'destination' from user input and map them to the Official List.
    Input: "{request.user_message}"
    Rules:
    - If origin is missing, use "CURRENT_LOCATION".
    - Language: zh-TW.
    - Return RAW JSON ONLY.

    Official List: [{context_str}]
    """

    try:
        # --- AI Processing ---
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        
        raw_text = response.text.strip()
        # Handle potential markdown backticks from AI
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
            
        intent_data = json.loads(raw_text)
        
        # --- Database & Maps Logic ---
        dest_name = intent_data.get("destination")
        orig_name = intent_data.get("origin")
        
        dest_coord = get_location_coords(dest_name)
        orig_coord = "CURRENT_LOCATION" if orig_name == "CURRENT_LOCATION" else get_location_coords(orig_name)

        if not dest_coord:
            return {"status": "error", "message": f"Place '{dest_name}' not recognized in DB."}

        # Calculate routing if origin is specified
        if orig_coord and orig_coord != "CURRENT_LOCATION":
            routing_data = get_travel_time(orig_coord, dest_coord, mode="walking")
        else:
            routing_data = {"info": "Request GPS from User.", "dest_coords": dest_coord}

        return {
            "status": "success",
            "parsed_intent": intent_data,
            "routing": routing_data
        }

    except genai.errors.ClientError as ce:
        print(f"[Vertex AI Error] {ce}")
        raise HTTPException(status_code=500, detail="Cloud AI Service Error.")
    except Exception as e:
        print(f"[Runtime Error] {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error.")