import time
import csv
from geopy.geocoders import Nominatim

# 1. Load the list of building names from a text file
file_path = "buildings.txt"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        buildings = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"File not found: {file_path}. Please make sure the file is in the same directory as this script.")
    exit()

# 2. Initialize Nominatim API (OpenStreetMap)
# OSM requires setting a user_agent to identify your application
geolocator = Nominatim(user_agent="campus_navigation_bot")

results = []

print(f"Preparing to fetch coordinates for {len(buildings)} locations...")
print("⚠️ Reminder: To comply with OSM regulations, each request will pause for 1.5 seconds. Please be patient.\n")

for building in buildings:
    # 💡 Tip: Add "中央大學" as a prefix, otherwise OSM might return thousands of "administrative buildings" worldwide
    search_query = f"中央大學 {building}"
    
    try:
        # Send a query request to OSM to get the coordinates of the building
        location = geolocator.geocode(search_query)
        
        if location:
            print(f"✅ Success: {building} -> Latitude: {location.latitude:.6f}, Longitude: {location.longitude:.6f}")
            results.append((building, location.latitude, location.longitude))
        else:
            print(f"❌ Not found: {building} (This location might not be tagged in OSM)")
        
        # Strictly comply with OSM API limits (do not remove sleep)
        time.sleep(1.5)
        
    except Exception as e:
        print(f"⚠️ Error occurred ({building}): {e}")
        time.sleep(2)

# 3. Save the successfully fetched results to a CSV file
output_file = "buildings_coordinates.csv"
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "latitude", "longitude"])
    writer.writerows(results)

print(f"\n🎉 Fetching completed! Successfully found {len(results)} locations.")
print(f"Results have been saved to {output_file}. You can open it to check the details!")