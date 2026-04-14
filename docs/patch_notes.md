# 專案架構
campus-navigation/
├── app/
│   ├── main.py            (總機：啟動 FastAPI 與 CORS 設定)
│   ├── api/routes.py      (服務生：接收請求，去資料庫拿圖，呼叫演算法)
│   ├── services/dijkstra.py (主廚：純粹的 Dijkstra 演算法模組)
│   └── models/schemas.py  (合約：定義 API 回傳的 JSON 格式)
├── data/
│   └── campus.db          (資料庫)
├── scripts/
│   └── init_db.py         (建商：用來自動生成資料表與初始地點資料的腳本)
├── .gitignore             (隱形斗篷：保護機密與本機資料庫不上傳)
├── requirements.txt       (購物清單：紀錄 FastAPI 等必備套件)
└── README.md              (說明書：專案門面與快速啟動指南)

# 2026/03/19
1. 打造核心引擎: 成功利用 Python 字典定義了微型校園地圖（通訊系館周邊），並實作了 Dijkstra 演算法來算出最短時間與路徑。
2. API 服務化與測試：導入 FastAPI，成功將演算法包裝成網頁 API，並學會使用內建的 Swagger UI (/docs) 來進行互動式測試與查看自動生成的文件。
3. 前端介面串接 (MVP)：寫了一個簡單的 index.html 網頁，利用 JavaScript 成功呼叫本機 API，把冰冷的 JSON 資料轉換成使用者看得懂的導航畫面。
4. 開源架構重構：將程式碼進行了專業的「關注點分離 (Separation of Concerns)」，並補齊了開源專案必備的 .gitignore 與 requirements.txt。
5. 升級關聯式資料庫：捨棄了寫死的 JSON 檔案，成功導入 SQLite 資料庫！寫了初始化腳本建立關聯式資料表，讓系統正式升級為「資料庫驅動」，為未來擴展全校地圖打下完美地基。


# 2026/04/02
1. 資料獲取革命：捨棄了效率較低的 geopy 逐一查詢，改用 Overpass Turbo (OSM API) 進行區域性座標抓取，成功獲取中大校區 130+ 個關鍵地標（系館、宿舍、餐廳、超商）。

2. 資料庫架構升級：重新設計 SQLite locations 資料表，導入 lat (緯度) 與 lon (經度) 欄位，讓系統具備真實世界定位能力。

3. 拓撲自動化生成：撰寫 auto_generate_paths.py，利用 Haversine 空間距離演算法，自動將 150 公尺內的地點建立連線，解決了手動建檔數百條路線的困境。

4. 後端引擎同步：更新 init_db.py 腳本，實現「一鍵重建資料庫」，讓 CSV 數據能完美轉化為 Dijkstra 演算法可用的圖形結構。

地圖視覺化 (Immediate)：申請 Google Maps JavaScript API，將經緯度座標渲染在真實地圖上，並畫出動態導航紅線。

AI 語意搜尋：引進 LLM (如 OpenAI/Gemini) 解析使用者的模糊需求，例如：「我想去喝杯手搖飲」自動導向至校內的「清心」或「夏克奶茶」。

AR 校園導航：長遠來看，可以結合行動裝置鏡頭，實現擴增實境 (AR) 的路徑指引。

digiRunner 企業級佈署：將 API 註冊至 digiRunner 管理平台，學習業界 API Gateway 的流量控管、身分驗證與監控流程。

# 2026/04/07

AI 配額與頻率優化 (Quota Management)

問題：Gemini 2.0 Free Tier 頻繁觸發 429 錯誤（Token 限制）。

對策：導入 SQLite 關鍵字過濾機制，將原本 150+ 地點的 Prompt 壓縮至 15 個以內，降低 90% 的 Token 消耗；並升級至最新的 gemini-2.5-flash 模型。

身分驗證轉型 (Authentication)

問題：API Key 模式不穩定且易過期。

對策：捨棄 API Key，改採 GCP 企業級的 Vertex AI (ADC/Service Account) 驗證模式，確保連線的高可靠性。

環境與權限配置 (Cloud Configuration)

問題：遇到 403 (API 未啟用) 與 404 (區域模型路徑錯誤)。

對策：手動啟用 aiplatform.googleapis.com 服務，並將模型部署區域鎖定在穩定的 us-central1。

網路層解析修正 (Network/DNS)

問題：Anaconda 環境中發生 11004 DNS 解析錯誤（無法連接 OAuth2）。

對策：透過強制同步 Quota Project 並優化 Python 環境的網路請求邏輯，解決了連線池解析失效問題。