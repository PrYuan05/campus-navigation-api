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
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# Import your Google Maps service
from app.maps_service import get_travel_time 
from app.path_utils import get_landmarks_along_route

load_dotenv()
app = FastAPI()

# Add CORS Middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    - ALWAYS resolve student abbreviations/aliases to their official names (e.g., "工一" -> "工程一館", "文一" -> "文學一館", "管二" -> "管理學院二館", "總圖" -> "總圖書館").
    - After resolving, your returned 'origin' and 'destination' MUST exactly match items in the Official List if possible.
    - If origin is missing natively, use "CURRENT_LOCATION".
    - If a place is completely unrecognized and not in the list, just return what the user said.
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
        
        if orig_name == "CURRENT_LOCATION":
            orig_coord = "CURRENT_LOCATION"
        else:
            orig_coord = get_location_coords(orig_name)

        if not dest_coord:
            return {"status": "error", "message": f"目的地 '{dest_name}' 無法在資料庫中找到。"}
            
        if orig_name != "CURRENT_LOCATION" and not orig_coord:
            return {"status": "error", "message": f"起點 '{orig_name}' 無法在資料庫中找到。"}

        # Calculate routing if origin is specified
        if orig_coord and orig_coord != "CURRENT_LOCATION":
            routing_data = get_travel_time(orig_coord, dest_coord, mode="walking")
            
            if routing_data.get("status") == "success" and routing_data.get("steps"):
                raw_steps = routing_data.get("raw_steps", [])
                landmarks = get_landmarks_along_route(raw_steps, exclude_names=[orig_name, dest_name])
                landmarks_str = "、".join(landmarks) if landmarks else "無特別知名地標"
                
                steps_str = "\n".join(routing_data["steps"])
                narrative_prompt = f"""
                你是一個親切的中央大學校園導航助理。
                請根據以下的 Google Maps 步行路線步驟，用流暢且友善自然的口語（繁體中文），寫成一段給使用者的導覽解說。
                起點名稱：{orig_name}
                終點名稱：{dest_name}
                總距離：{routing_data.get('distance_text')}
                預計時間：{routing_data.get('duration_text')}
                沿途經過的地標有：{landmarks_str}
                
                路線步驟：
                {steps_str}
                
                注意：
                - 用一段精簡俐落的話描述即可，廢話不要太多，維持友善態度。
                - 請自然地將沿途經過的地標融入敘述中，當作讓使用者參考的路標。
                - 請使用中央大學學生的在地稱呼（簡稱）來稱呼建築物以增加親切感。例如將「工程一館」簡稱呼為「工一」，「管理學院二館」稱呼為「管二」，「科學二館」為「科二」，宿舍名稱也請簡化（如女十四舍為女14）。
                - 不要只是條列式輸出，請用順暢的段落描述。
                - 直接回覆導覽文字，不要包含任何 json 格式，純文字即可。
                """
                try:
                    narrative_res = client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=narrative_prompt,
                    )
                    routing_data["info"] = narrative_res.text.strip()
                except Exception as ex:
                    print(f"[Narrative Generation Error] {ex}")
                    pass
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