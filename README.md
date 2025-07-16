# FB 租屋過濾器

## 啟動方式
### 1. 安裝後端
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. 啟動 Ollama
```bash
複製
編輯
ollama serve
ollama run mistral
```

### 3. 安裝 Chrome 擴充
打開 Chrome → 擴充功能 → 管理擴充程式
開啟「開發人員模式」
載入「未封裝項目」→ 選擇 extension/ 資料夾

### 4. 設定條件
點擊擴充圖示 → 填寫預算、地點、條件 → 儲存

### 5. 開啟 FB 社團
每 10 秒擷取貼文 → 呼叫 API → 若符合條件，會顯示通知

## ✅ **啟動測試**
1. 啟動後端 + Ollama  
2. 載入 Chrome 擴充 → 設定條件  
3. 開啟 FB 社團  
4. 如果有符合條件的貼文 → **桌面通知**:w
5. 
