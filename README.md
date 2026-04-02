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
初始化資料庫

Bash
python scripts/auto_generate_paths.py  # 自動生成路徑
python scripts/init_db.py              # 重建資料庫
啟動伺服器

Bash
uvicorn app.main:app --reload
前往 http://127.0.0.1:8000/docs 開始測試！

📂 專案結構
app/: API 核心邏輯與演算法。

data/: 存放原始 CSV 圖資與 SQLite 資料庫。

scripts/: 資料處理與資料庫維護腳本。

Developed with ❤️ by NCU Communication Engineering Student (李元皓)


---

為了讓你對整個專案的進度與未來規劃更有方向感，我準備了一個「專案進度與願景互動看板」。你可以點擊不同的階段，查看我們已經完成了哪些技術細節，以及未來還有哪些挑戰需要克服。

```json?chameleon
{"component":"LlmGeneratedComponent","props":{"height":"700px","prompt":"建立一個「專案里程碑與願景互動看板」。\n\n1. 核心邏輯 (Explorer 模式)：\n   - 分為四個主要階段：\n     - 【第一階段：核心引擎 (已完成)】：Dijkstra 演算法、FastAPI 基礎架構、文字導航回傳。\n     - 【第二階段：資料革命 (進行中)】：OSM 座標抓取、SQLite 空間欄位升級、150m 空間拓撲自動連線。\n     - 【第三階段：視覺化整合 (下一步)】：Google Maps JavaScript API、座標反查渲染、動態紅線繪製。\n     - 【第四階段：智慧化與部署 (長期)】：AI 語意解析意圖、OpenAI API 整合、digiRunner 平台註冊。\n\n2. 交互功能：\n   - 點擊每個階段的標題，下方會動態顯示該階段的「技術關鍵點 (Key Techs)」與「達成目標 (Goals)」。\n   - 提供一個「完成進度條」，視覺化展示目前專案的成熟度。\n   - 包含一個「NCU 專屬視角」：強調這些技術如何應用在中央大學通訊系的專題背景中。\n\n3. 視覺要求：\n   - 使用卡片式佈局。\n   - 用不同的標記區分「已完成」、「進行中」與「計畫中」。\n   - 整體風格需具備科技感與工程專業感。\n\n4. 語言：繁體中文。","id":"im_669d0833f2dd1b52"}}