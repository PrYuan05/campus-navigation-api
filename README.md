# 📍 NCU Campus Navigation API (中央大學智慧校園導航系統)

![Project Status](https://img.shields.io/badge/Status-Development-orange)
![Python Version](https://img.shields.io/badge/Python-3.9+-blue)
![Framework](https://img.shields.io/badge/Framework-FastAPI-green)

這是一個為 **中央大學** 量身打造的智慧化導航後端系統。透過 Dijkstra 演算法與真實地理座標 (OSM)，提供校內系館、宿舍及生活圈的最短路徑規劃。

## 🌟 核心特色

- **資料庫驅動**：使用 SQLite 管理 130+ 個校園地標座標。
- **自動化拓撲**：利用 Haversine 演算法自動計算空間鄰近性並構建導航路徑。
- **高效能導航**：實作 Dijkstra 最短路徑演算法，支援步行時間預估。
- **標準 API 規範**：基於 FastAPI 開發，內建 Swagger 互動式文件。

## 🛠️ 技術棧

- **Backend**: Python, FastAPI, Uvicorn
- **Algorithm**: Dijkstra's Algorithm, Haversine Formula
- **Database**: SQLite3
- **Data Source**: OpenStreetMap (via Overpass Turbo)
- **Library**: Geopy, Pydantic

## 🚀 快速啟動

1. **環境建置**
   ```bash
   python -m venv .venv
   source .venv/Scripts/activate  # Windows
   pip install -r requirements.txt

2. **初始化資料庫**
   ```bash
   python scripts/auto_generate_paths.py  # 自動生成路徑
   python scripts/init_db.py              # 重建資料庫


3. **啟動伺服器**
   ```bash
   uvicorn app.main:app --reload

前往 http://127.0.0.1:8000/docs 開始測試！

📂 專案結構
app/: API 核心邏輯與演算法。

data/: 存放原始 CSV 圖資與 SQLite 資料庫。

scripts/: 資料處理與資料庫維護腳本。

Developed with ❤️ by NCU Communication Engineering Student (李元皓)