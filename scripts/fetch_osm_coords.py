import time
import csv
from geopy.geocoders import Nominatim

# 1. 讀取建築物清單
file_path = "buildings.txt"
try:
    with open(file_path, "r", encoding="utf-8") as f:
        buildings = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"找不到 {file_path}，請確認檔案與程式在同一目錄。")
    exit()

# 2. 初始化 Nominatim API (OpenStreetMap)
# OSM 規定必須設定 user_agent 來識別你的應用程式
geolocator = Nominatim(user_agent="campus_navigation_bot")

results = []

print(f"準備抓取 {len(buildings)} 個地點的座標...")
print("⚠️ 提醒：為遵守 OSM 規範，每筆請求將暫停 1.5 秒，請耐心等候。\n")

for building in buildings:
    # 💡 核心技巧：加上「中央大學」作為前綴，否則 OSM 在全世界會搜出幾千個「行政大樓」
    search_query = f"中央大學 {building}"
    
    try:
        # 向 OSM 發送查詢請求
        location = geolocator.geocode(search_query)
        
        if location:
            print(f"✅ 成功: {building} -> 緯度: {location.latitude:.6f}, 經度: {location.longitude:.6f}")
            results.append((building, location.latitude, location.longitude))
        else:
            print(f"❌ 找不到: {building} (OSM 圖資上可能沒有這個標籤)")
        
        # 嚴格遵守 OSM API 限制 (絕對不能拿掉 sleep)
        time.sleep(1.5)
        
    except Exception as e:
        print(f"⚠️ 發生錯誤 ({building}): {e}")
        time.sleep(2)

# 3. 將成功抓取的結果存成 CSV 檔案
output_file = "buildings_coordinates.csv"
with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "latitude", "longitude"])
    writer.writerows(results)

print(f"\n🎉 抓取完成！成功找到 {len(results)} 個地點。")
print(f"結果已存入 {output_file}，你可以打開來檢查看看！")