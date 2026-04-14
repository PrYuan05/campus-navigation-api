import os
import requests
from dotenv import load_dotenv

# load .env file to get API keys
load_dotenv()

# Safely get API Key
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

def get_travel_time(origin, destination, mode="walking"):
    """
    Calculate travel time and distance between two points
    mode: can be 'walking' (步行), 'driving' (開車), 'transit' (大眾運輸)
    """
    if not API_KEY:
        return {"error": "API Key not found, please check the .env file"}

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": mode,
        "language": "zh-TW", # Return results in Traditional Chinese
        "key": API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Check if API status is OK
        if data["status"] == "OK":
            elements = data["rows"][0]["elements"][0]
            
            if elements["status"] == "OK":
                return {
                    "status": "success",
                    "origin": data["origin_addresses"][0],
                    "destination": data["destination_addresses"][0],
                    "distance_text": elements["distance"]["text"],     # e.g., "1.2 km"
                    "duration_text": elements["duration"]["text"],     # e.g., "15 mins"
                    "duration_seconds": elements["duration"]["value"]  # Duration in seconds, useful for backend calculations
                }
            else:
                return {"error": f"Unable to calculate route: {elements['status']}"}
        else:
             return {"error": f"API error: {data['status']}"}
             
    except Exception as e:
        return {"error": f"Request exception: {str(e)}"}