# 🏫 NCU Campus Navigation API (OpenTPI)

這是一個專為中央大學設計的智能語意導航系統，包含強健的 FastAPI 後端與順暢的 React 前端介面。使用者可以透過自然語言（例如：「我要從依仁堂去大禮堂」）進行詢問，系統會自動辨識校園建築物、查詢精確座標，並串接 Google Maps Directions API 計算最優步行路徑，再透過 Gemini 生成口語化且豐富的沿途導航指引。

## 🌟 核心功能

- **自然語言辨識 (NLU) 與防呆機制**：使用 Google Vertex AI (Gemini 2.5 Flash) 進行地點對齊與意圖分析，並具備完善的輸入驗證與防呆處理機制。
- **口語化情境導航**：結合 Google Maps Directions API 取得 Turn-by-Turn 路線，再透過大型語言模型渲染成生動、具備校園地標的口語化導航指引。
- **校園資料庫**：內建 SQLite 支援 150+ 個校園地點的精確座標查詢。
- **Token 優化與前後端整合**：自研關鍵字過濾演算法降低成本，且現已完成前端應用整合以提供完整的互動體驗。

## 📁 目錄結構

```text
campus-navigation-api/
├── frontend/               # 前端專案原始碼 (React + Vite)
├── app/                    # 後端核心程式碼
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

- **Frontend**: React, Vite, Node.js
- **Backend**: Python, FastAPI, Uvicorn
- **AI & Maps**: Google Vertex AI (Gemini), Google Maps Directions API
- **Database**: SQLite3
- **Package Management**: `uv`, `npm`
- **Deployment**: Digirunner

## 🚀 快速啟動

### 1. 後端 API 伺服器建置 (Backend)

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

### 2. 前端開發伺服器建置 (Frontend)

確認已安裝 Node.js 環境後，進入前端目錄：

```bash
cd frontend
npm install
# 啟動前端開發伺服器
npm run dev
```

## 📂 專案結構補充說明

- `frontend/`: 基於 React 的前端使用者介面。
- `app/`: 後端核心邏輯與演算法，提供穩定的導航對話服務。
- 其餘 `data/`, `scripts/`, `docs/`, `tests/` 維持原有用途供資料開發與自動化測試使用。

_未來正式環境將透過 Digirunner 進行部署。_

Developed with ❤️ by NCU Communication Engineering Student (李元皓)
