from google import genai
from dotenv import load_dotenv
import os

# 載入 API Key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 測試用的假訊息
test_message = "轉傳！台灣健保即將取消，請大家趕快去醫院拿藥存起來！"

# 設計給 Gemini 的指令
prompt = f"""
你是一個台灣假訊息判別專家。
請分析以下這段文字是否可能是假訊息或詐騙訊息。

文字內容：
{test_message}

請用以下 JSON 格式回答：
{{
  "機率": "85%",
  "判斷": "可能是假訊息",
  "可疑點": ["可疑點1", "可疑點2", "可疑點3"],
  "建議": "不要轉傳，可至台灣事實查核中心查證"
}}

只回傳 JSON，不要其他文字。
"""

# 呼叫 Gemini
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt
)

print(response.text)