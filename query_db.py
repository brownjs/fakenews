import chromadb

# 連接到剛剛建立好的本地資料庫
client = chromadb.PersistentClient(path="./chroma_db")

# 取得 collection
collection = client.get_collection(name="fake_news")

# 你想測試查詢的句子
query = "l政府要取消健保，大家快去囤藥"

# 查詢最相近的 3 筆
results = collection.query(
    query_texts=[query],
    n_results=3
)

print("🔍 你的查詢：", query)
print("\n最相近的結果：")

for i, doc in enumerate(results["documents"][0], start=1):
    print(f"{i}. {doc}")