# 🏫 NCU Campus Navigation API (OpenTPI)

[中文版說明請見下方](#-中文版說明-traditional-chinese-version)

This is an intelligent semantic navigation system designed specifically for National Central University (NCU), featuring a robust FastAPI backend and a smooth React frontend interface. Users can ask for directions using natural language (e.g., "I want to go from Yiren Hall to the Auditorium"), and the system automatically identifies campus buildings, queries precise coordinates, integrates with the Google Maps Directions API to calculate the optimal walking route, and finally uses Gemini to generate conversational and rich en-route navigation instructions.

This project collaborates deeply with the open-source community **OpenTPI**, utilizing the enterprise-grade API/AI gateway **digiRunner** as the core for security and traffic management.

## 🌐 OpenTPI Resource Links

- Official Website: [OpenTPI](https://tpi.dev/)
- GitHub: [Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) (Feel free to check the License, README to contribute, or ask questions in the discussion area!)
- Documentation: [docs.tpi.dev](https://docs.tpi.dev/)
- LinkedIn: [OpenTPI LinkedIn](https://www.linkedin.com/company/106457186) (Follow us for the latest news!)

## 🌟 Core Value and Benefits

- **Campus Localization**: Accurately aligns with NCU student jargon (e.g., "Engineering 1", "Management 2"), providing precise location parsing unmatched by generic maps.
- **Humanized Guidance**: Transforms rigid navigation steps into landmark-referenced paragraphs, making walking directions more intuitive.
- **Accessibility**: Voice input and TTS (Text-to-Speech) capabilities allow users to navigate "by ear" while walking on campus, enhancing safety and convenience.
- **Development Efficiency & Flexibility**: Modular architecture combined with digiRunner gateway management facilitates future feature expansion and AI Token usage monitoring.

## 🏗️ Architecture and Workflow

### 1️⃣ Functional Module Architecture
The system consists of four core modules:
- **UI Interaction Module (Frontend)**: React + Vite, integrating Web Speech API for voice recognition (STT) and voice synthesis (TTS).
- **API Gateway & Security Module (digiRunner)**: Handles request filtering, API Key authentication, rate limiting, and log monitoring between frontend and backend, protecting backend and AI resources.
- **AI Semantic Analysis Engine (NLU Engine)**: Powered by Gemini 2.5 Flash, responsible for intent extraction and location entity alignment (translating colloquial terms into system-recognizable locations).
- **Navigation & Campus Map Module (Routing & Knowledge)**: SQLite local campus database paired with Google Maps Directions API to calculate routes and fetch landmarks within 50m of the path.

### 2️⃣ Data Flow
1. **Source**: User inputs voice or text via the frontend.
2. **Gateway**: Frontend sends the request to the **digiRunner gateway** for security and traffic validation.
3. **Process**: Upon authentication, the FastAPI backend receives the request. It uses Vertex AI (Gemini) for NLU intent analysis to extract origin and destination.
4. **Compute**: The backend queries SQLite for precise coordinates, calls Google Maps for walking routes, and fetches en-route landmarks.
5. **Synthesis**: The raw route and landmark info are fed back to Gemini to render localized, conversational navigation text.
6. **Output**: JSON formatted results are returned to the frontend via digiRunner, displayed on the UI, and played via the TTS engine.

## 📁 Directory Structure

```text
campus-navigation-api/
├── frontend/               # Frontend source code (React + Vite)
├── app/                    # Backend core code
│   ├── main.py             # FastAPI routes & AI logic
│   └── maps_service.py     # Google Maps API wrapper
├── data/                   # Data storage (Database & Map Info)
├── docs/                   # Project documentation
├── scripts/                # Automation & Maintenance scripts
├── tests/                  # Test scripts
├── .env.example            # Environment variables example
├── requirements.txt        # Python dependencies
├── docker-compose.yml      # Production Deployment Configuration
├── nginx.conf              # Nginx Proxy Configuration
├── LICENSE                 # License terms
└── README.md
```

## 🛠️ Technology Stack

- **Frontend**: React, Vite, Web Speech API, TailwindCSS
- **Backend**: Python, FastAPI, Uvicorn
- **Gateway**: [digiRunner](https://tpi.dev/) (API & AI Gateway)
- **AI & Maps**: Google Vertex AI (Gemini 2.5 Flash), Google Maps Directions API
- **Deployment**: Docker, Nginx (Reverse Proxy)
- **Database**: SQLite3
- **Package Management**: `uv`, `npm`

## 🚀 Quick Start

### 1. Backend API Server Setup

This project uses `uv` for fast and secure python package management.

```bash
uv venv .venv
.venv\Scripts\activate  # Windows environment activation
uv pip install -r requirements.txt
```

**(Optional) Database Initialization**

```bash
uv run python scripts/auto_generate_paths.py  # Auto-generate paths
uv run python scripts/init_db.py              # Rebuild database
```

**Start FastAPI Server**

```bash
uv run uvicorn app.main:app --reload
```

Backend Testing URL: `http://127.0.0.1:8000/docs`

### 2. Frontend Development Server

Ensure Node.js is installed, then enter the frontend directory:

```bash
cd frontend
npm install
npm run dev
```

### 3. Production Deployment (Docker + digiRunner)

The production environment is packaged via Docker. Nginx serves the React build and proxies API requests.
1. Build frontend: `npm run build` inside the `frontend` folder.
2. Ensure digiRunner container is running on the host network.
3. Deploy services: `docker compose up -d`
4. Access via `http://<YOUR_IP>`

---

# 🇹🇼 中文版說明 (Traditional Chinese Version)

這是一個專為中央大學設計的智能語意導航系統，包含強健的 FastAPI 後端與順暢的 React 前端介面。使用者可以透過自然語言（例如：「我要從依仁堂去大禮堂」）進行詢問，系統會自動辨識校園建築物、查詢精確座標，並串接 Google Maps Directions API 計算最優步行路徑，再透過 Gemini 生成口語化且豐富的沿途導航指引。

本專案與開源社群 **OpenTPI** 深度合作，並將導入企業級 API/AI 網關 **digiRunner** 作為安全與流量管理核心。

## 🌐 OpenTPI 資源連結

- 官方網站：[OpenTPI](https://tpi.dev/)
- GitHub：[Physical-Intelligence/openpi](https://github.com/Physical-Intelligence/openpi) (歡迎查看 License、README 參與貢獻，或在 discussion 區提問！)
- 文件中心 (Documentation)：[docs.tpi.dev](https://docs.tpi.dev/)
- LinkedIn：[OpenTPI LinkedIn](https://www.linkedin.com/company/106457186) (歡迎追蹤獲取最新資訊！)

## 🌟 核心價值與效益

- **校園在地化**：精準對齊 NCU 學生慣用語（如「工一」、「管二」），提供一般通用地圖無法比擬的精確地點解析。
- **人性化指引**：將冷硬的導航步驟轉化為「經過圖書館後右轉」等具備地標參考的段落，更符合步行直覺。
- **無障礙交互**：語音輸入與 TTS 語音回覆功能，讓使用者在校園穿梭時能「用聽的」導航，提升安全性與便利性。
- **開發效率與彈性**：模組化架構加上 digiRunner 網關管理，便於未來擴充功能與監控 AI Token 使用量。

## 🏗️ 系統架構與流程

### 1️⃣ 功能模組架構
系統由四大核心模組組成，各司其職：
- **UI 互動呈現模組 (Frontend)**：React + Vite，結合 Web Speech API 提供語音辨識 (STT) 與語音合成 (TTS)。
- **API 網關與安全模組 (digiRunner)**：負責前端與後端之間的請求過濾、API Key 認證、流量限制與日誌監控，保護後端與 AI 資源。
- **AI 語意分析引擎 (NLU Engine)**：基於 Gemini 2.5 Flash，負責意圖提取與地名實體對齊（將口語轉化為系統可識別的地點）。
- **導航與校園圖資模組 (Routing & Knowledge)**：SQLite 本地校園資料庫搭配 Google Maps Directions API，負責計算路徑並抓取沿途地標。

### 2️⃣ 操作流程與資料流
1. **收集 (Source)**：使用者透過前端語音或文字輸入（如「我想從工一走到管二」）。
2. **傳輸 (Gateway)**：前端將請求發送至 **digiRunner 網關**，進行安全與流量校驗。
3. **分析 (Process)**：認證通過後，FastAPI 後端接收請求。利用 Vertex AI (Gemini) 進行 NLU 意圖分析，提取出 `origin: "工程一館"` 與 `destination: "管理學院二館"`。
4. **計算 (Compute)**：後端查詢 SQLite 取得精確座標，並呼叫 Google Maps 規劃步行路徑，抓取沿途 50m 內地標。
5. **渲染 (Synthesis)**：將原始路徑與地標資訊再次交由 Gemini，渲染成在地化、口語化的導覽文字（如「好的！從工一出發，會經過總圖...」）。
6. **輸出 (Output)**：JSON 格式的結果透過 digiRunner 回傳前端，前端介面顯示並透過 TTS 引擎播放語音。

## 🚀 快速啟動

### 1. 後端 API 伺服器建置

本專案後端開發流程已轉換至使用效能更快、更安全的 `uv` 作為套件管理工具。

```bash
uv venv .venv
.venv\Scripts\activate  # Windows 環境啟用
uv pip install -r requirements.txt
```

**(選用) 初始化資料庫**

```bash
uv run python scripts/auto_generate_paths.py  # 自動生成路徑
uv run python scripts/init_db.py              # 重建資料庫
```

**啟動 FastAPI 伺服器**

```bash
# 請確保處於專案根目錄
uv run uvicorn app.main:app --reload
```

後端測試入口：http://127.0.0.1:8000/docs

### 2. 前端開發伺服器建置

確認已安裝 Node.js 環境後，進入前端目錄：

```bash
cd frontend
npm install
# 啟動前端開發伺服器
npm run dev
```

### 3. 雲端正式部署 (Docker + digiRunner)

正式環境將透過 Docker 進行完整打包部署。透過 Nginx 代理前端靜態文件與 API 請求。
1. 前端編譯：在 `frontend` 資料夾內執行 `npm run build`
2. 確保 digiRunner 容器已在宿主機網路中運行
3. 部署服務：執行 `docker compose up -d`
4. 訪問：直接開啟機器的公開 IP (`http://<YOUR_IP>`)

---
Developed with ❤️ by NCU Communication Engineering Student (李元皓)
