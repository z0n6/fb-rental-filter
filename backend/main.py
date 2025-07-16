from fastapi import FastAPI, Body
from pydantic import BaseModel
import re
import requests
import json

app = FastAPI()

# ---------- 輸入資料模型 ----------
class AnalyzeRequest(BaseModel):
    text: str
    prefs: dict

# ---------- 工具函式 ----------
def extract_price(text: str):
    """從貼文中抓取租金"""
    match = re.search(r"([1-9]\d{3,5})", text)
    return int(match.group(1)) if match else None

def check_location(text: str, locations: list):
    """檢查是否包含任何地點關鍵字"""
    return any(loc in text for loc in locations if loc.strip())

def extract_json(text: str):
    """從 LLM 回傳文字中安全擷取 JSON"""
    try:
        json_match = re.search(r"\{[\s\S]*\}", text)  # 找到 JSON 區塊
        if json_match:
            return json.loads(json_match.group(0))
    except:
        pass
    return None

# ---------- API ----------
@app.post("/analyze_post")
async def analyze_post(req: AnalyzeRequest):
    text = req.text
    prefs = req.prefs or {}

    # 解析使用者設定
    budget_range = prefs.get("budget", "10000-20000").split("-")
    try:
        min_price, max_price = map(int, budget_range)
    except ValueError:
        min_price, max_price = 10000, 20000

    location_keywords = prefs.get("location", "").split(",")
    extras = prefs.get("extras", "")

    # Step 1: 初步過濾
    price = extract_price(text)
    if not price or price < min_price or price > max_price:
        return {"relevant": False, "summary": "", "reason": "租金不符合"}

    if not check_location(text, location_keywords):
        return {"relevant": False, "summary": "", "reason": "地點不符合"}

    # Step 2: LLM 判斷
    prompt = f"""
你是一個房屋租賃過濾助手，請只輸出 JSON 格式。
使用者需求：
- 預算：{prefs.get('budget')}
- 地點：{prefs.get('location')}
- 額外條件：{extras}

請判斷以下貼文是否符合需求，輸出 JSON 格式：
{{
  "relevant": true/false,
  "reason": "為什麼符合或不符合",
  "summary": "地點、租金、主要特點"
}}
貼文內容：{text}
"""

    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "llama3.2",  # 或 "llama2"
            "prompt": prompt,
            "stream": False  # 關閉流式回傳
        })
        llm_data = response.json()
        llm_text = llm_data.get("response", "").strip()
    except Exception as e:
        return {"relevant": False, "summary": "", "reason": f"LLM 錯誤: {str(e)}"}

    # 嘗試解析 LLM 回傳 JSON
    parsed = extract_json(llm_text)
    if parsed:
        relevant = parsed.get("relevant", False)
        summary = parsed.get("summary", text[:50])
        reason = parsed.get("reason", "")
    else:
        # Fallback
        relevant = "true" in llm_text.lower()
        summary = text[:50]
        reason = llm_text

    return {
        "relevant": relevant,
        "summary": summary,
        "reason": reason
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}
