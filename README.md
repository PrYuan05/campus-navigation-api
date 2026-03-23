# 📍 微型校園導航 API (Campus Navigation API)

這是一個基於 Python 與 FastAPI 開發的校園路線導航後端 API 專案。
旨在解決新生或外系同學在校園內尋找特定教室或系館時迷路的問題。未來預計整合至 API 管理平台 (如 digiRunner) 以提供更穩定、安全的微服務。

## ✨ 核心特色 (Features)
* **極速計算**：底層採用 Dijkstra 演算法，能瞬間找出兩點之間的最短/最快路徑。
* **資料與邏輯分離**：地圖節點與權重資料獨立儲存於 `data/campus_map.json`，極度容易擴展與維護。
* **RESTful API**：提供標準的 HTTP GET 介面與 JSON 格式回應，方便任何前端 (Web/iOS/Android) 輕鬆串接。
* **內建互動文件**：自帶 Swagger UI，啟動後可直接在瀏覽器進行 API 測試。

## 🛠️ 技術棧 (Tech Stack)
* **後端框架**: Python 3.x, FastAPI
* **伺服器**: Uvicorn
* **演算法**: Dijkstra's Algorithm

## 🚀 快速開始 (Quick Start)

### 1. 安裝依賴套件
請確保你的電腦已安裝 Python，接著在終端機輸入以下指令安裝所需套件：
```bash
pip install fastapi uvicorn
