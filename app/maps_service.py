import os
import requests
import re
from dotenv import load_dotenv

# load .env file to get API keys
load_dotenv()

# Safely get API Key
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_travel_time(origin, destination, mode="walking"):
    """
    Calculate travel route and time between two points using Directions API
    mode: can be 'walking' (步行), 'driving' (開車), 'transit' (大眾運輸)
    """
    if not API_KEY:
        return {"error": "API Key not found, please check the .env file"}

    url = "https://maps.googleapis.com/maps/api/directions/json"
    
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "language": "zh-TW", # Return results in Traditional Chinese
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check if API status is OK
        if data["status"] == "OK" and data.get("routes"):
            leg = data["routes"][0]["legs"][0]
            
            # Extract html_instructions and strip HTML tags
            clean_steps = []
            raw_steps_coords = []
            for idx, step in enumerate(leg.get("steps", [])):
                raw_text = step.get("html_instructions", "")
                # Clean html tags
                clean_text = re.sub(r'<[^>]+>', '', raw_text)
                if clean_text:
                    clean_steps.append(f"{idx+1}. {clean_text}")
                    
                # Extract coordinates for landmark calculation
                start_loc = step.get('start_location', {})
                end_loc = step.get('end_location', {})
                raw_steps_coords.append({
                    'start_lat': start_loc.get('lat'),
                    'start_lng': start_loc.get('lng'),
                    'end_lat': end_loc.get('lat'),
                    'end_lng': end_loc.get('lng'),
                })
            
            return {
                "status": "success",
                "origin": leg["start_address"],
                "destination": leg["end_address"],
                "distance_text": leg["distance"]["text"],
                "duration_text": leg["duration"]["text"],
                "duration_seconds": leg["duration"]["value"],
                "steps": clean_steps,
                "raw_steps": raw_steps_coords
            }
        else:
             return {"error": f"API error: {data.get('status')} - {data.get('error_message', '')}"}
             
    except Exception as e:
        return {"error": f"Request exception: {str(e)}"}