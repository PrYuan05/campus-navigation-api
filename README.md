# 🏫 NCU Campus Navigation API (OpenTPI)

這是一個專為中央大學設計的語意導航後端系統。使用者可以透過自然語言（例如：「我要從依仁堂去大禮堂」）進行詢問，系統會自動辨識校園建築物、查詢精確座標，並串接 Google Maps API 計算最優步行路徑。

## 🌟 核心功能
- **自然語言辨識 (NLU)**：使用 Google Vertex AI (Gemini 2.5 Flash) 進行地點對齊與意圖分析。
- **校園資料庫**：內建 SQLite 支援 150+ 個校園地點的精確座標查詢。
- **即時導航數據**：整合 Google Maps Directions API，提供距離與步行預估時間。
- **Token 優化**：自研關鍵字過濾演算法，極大化 API 響應速度並降低成本。

## 📁 目錄結構
```text
campus-navigation-api/
├── app/                    # 核心程式碼
│   ├── main.py             # FastAPI 路由與 AI 邏輯
│   └── maps_service.py     # Google Maps API 封裝
├── data/                   # 資料存儲 (資料庫與圖資)
├── docs/                   # 專案文件 (版本紀錄)
├── scripts/                # 自動化與維護腳本
├── tests/                  # 測試腳本
├── .env.example            # 環境變數範例檔
├── requirements.txt        # 依賴套件清單
├── LICENSE                 # 授權條款
└── README.md
```

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
- `app/`: API 核心邏輯與演算法。
- `data/`: 存放原始 CSV 圖資與 SQLite 資料庫。
- `scripts/`: 資料處理與資料庫維護腳本。
- `docs/`: 專案相關文件與版本更新紀錄。
- `tests/`: 用於確保 API 健康度與外部連線的測試腳本。

Developed with ❤️ by NCU Communication Engineering Student (李元皓)