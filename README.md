# FastAPI + MySQL 開發專案

這是一個使用 **FastAPI** 框架與 **MySQL** 資料庫的後端專案，透過 **Docker Compose** 啟動資料庫，並使用 **pipenv** 管理 Python 虛擬環境。

---

## 📁 專案結構

\`\`\`
fastapi-mysql-backend/
├── fastapi-backend/          # FastAPI 應用程式
│   ├── main.py               # 主程式，定義 API 路由
│   ├── db.py                 # 資料庫連線設定
│   ├── schemas.py            # 資料格式與驗證模型
│   ├── Pipfile               # pipenv 虛擬環境定義
│   └── ...
│
└── mysql-project/            # MySQL 容器設定
    └── docker-compose.yml    # 啟動資料庫的 Docker 設定
\`\`\`

---

## 🚀 專案啟動流程

### 1️⃣ 啟動 MySQL 資料庫

\`\`\`bash
cd mysql-project
docker-compose up -d
\`\`\`

MySQL 預設設定：
- host: \`127.0.0.1\`
- port: \`3306\`
- user: \`testuser\`
- password: \`test123\`
- database: \`testdb\`

> 若你有使用 \`phpMyAdmin\`，可透過 \`http://localhost:8080\` 進行圖形化操作。

---

### 2️⃣ 啟動 FastAPI 應用程式

\`\`\`bash
cd ../fastapi-backend
pipenv install             # 安裝依賴（首次使用）
pipenv shell               # 進入虛擬環境
uvicorn main:app --reload  # 啟動開發伺服器
\`\`\`

> 預設埠號為 \`http://localhost:8000\`

---

### 3️⃣ 使用 Swagger UI 測試 API

開啟瀏覽器進入：

\`\`\`
http://localhost:8000/docs
\`\`\`

可以透過網頁介面操作 API，包括：
- 新增筆記（POST /notes）
- 查詢所有筆記（GET /notes）
- 更新或刪除筆記等功能（PUT, PATCH, DELETE）

---

##  其他注意事項

- 本專案使用 **pipenv** 管理依賴與虛擬環境
- 請搭配 \`.gitignore\` 忽略不要追蹤的檔案（快取、虛擬環境、設定檔等）

---

## 作者

HSU, YEN-WEI  
（Git 本地使用名稱設定為：\`mike\`）

---

## License

This project is licensed under the MIT License.
EOF
