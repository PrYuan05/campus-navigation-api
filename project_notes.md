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

# Works have been Done
1. 打造核心引擎: 成功利用 Python 字典定義了微型校園地圖（通訊系館周邊），並實作了 Dijkstra 演算法來算出最短時間與路徑。
2. API 服務化與測試：導入 FastAPI，成功將演算法包裝成網頁 API，並學會使用內建的 Swagger UI (/docs) 來進行互動式測試與查看自動生成的文件。
3. 前端介面串接 (MVP)：寫了一個簡單的 index.html 網頁，利用 JavaScript 成功呼叫本機 API，把冰冷的 JSON 資料轉換成使用者看得懂的導航畫面。
4. 開源架構重構：將程式碼進行了專業的「關注點分離 (Separation of Concerns)」，並補齊了開源專案必備的 .gitignore 與 requirements.txt。
5. 升級關聯式資料庫：捨棄了寫死的 JSON 檔案，成功導入 SQLite 資料庫！寫了初始化腳本建立關聯式資料表，讓系統正式升級為「資料庫驅動」，為未來擴展全校地圖打下完美地基。