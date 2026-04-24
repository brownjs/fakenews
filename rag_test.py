iimport chromadb
import requests
from chromadb.utils import embedding_functions

# 必須跟 build_db.py 用一樣的模型
multilingual_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_collection(
    name="fake_news",
    embedding_function=multilingual_ef
)
# =========================
# 2. 讓使用者輸入訊息
# =========================
user_input = input("請輸入訊息：").strip()

if not user_input:
    print("你沒有輸入任何訊息，程式結束。")
    exit()

# =========================
# 3. 查詢最相似的 3 筆資料
# =========================
results = collection.query(
    query_texts=[user_input],
    n_results=3
)

retrieved_docs = results["documents"][0]

print("\n🔍 找到的相似訊息：")
for i, doc in enumerate(retrieved_docs, start=1):
    print(f"{i}. {doc}")

# =========================
# 4. 把檢索結果組成 prompt
# =========================
context = "\n".join([f"{i+1}. {doc}" for i, doc in enumerate(retrieved_docs)])

prompt = f"""
你是一個台灣假訊息查核助手。

你的任務是：根據「使用者輸入」與「資料庫中找到的相似訊息」，做初步判斷。

【使用者輸入】
{user_input}

【資料庫中找到的相似訊息】
{context}

請嚴格遵守以下規則：
1. 只能根據我提供的資料回答
2. 不要補充外部網址、新聞、政府公告或任何未提供資訊
3. 如果資料不足，就明確寫「目前只能初步判斷」
4. 不要寫多餘解釋
5. 一定要按照指定格式輸出
6. 每一欄都只能輸出一行

請依照以下格式輸出，不能多寫任何前言、註解、說明：

可疑程度：低 / 中 / 高
判斷：可能是假訊息 / 資料不足，需進一步查證 / 暫時看不出明顯異常
可疑點：請用 2 到 3 個短語，用分號隔開
建議：先不要轉傳 / 查官方公告 / 查事實查核網站 / 需要更多資料

補充說明：
- 「可疑程度」不是機率，只是根據目前相似案例做出的初步判斷強度
- 「可疑點」必須是短語，不能寫完整長句
- 「可疑點」可從以下角度挑選：
  1. 與資料庫某則訊息高度相似
  2. 涉及突發政策變動
  3. 帶有恐慌或催促語氣
  4. 缺乏明確來源
  5. 與常見謠言模式相似
"""

# =========================
# 5. 呼叫 Ollama API
# =========================
try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    print("\n🤖 AI 判斷結果：\n")

    data = response.json()

    if "response" in data:
        print(data["response"])
    elif "error" in data:
        print("Ollama 錯誤：", data["error"])
    else:
        print("未知回傳格式：", data)

except requests.exceptions.ConnectionError:
    print("無法連接到 Ollama，請先確認 Ollama 有啟動。")
except requests.exceptions.Timeout:
    print("Ollama 回應逾時，模型可能正在忙或載入較久。")
except Exception as e:
    print("發生錯誤：", e)