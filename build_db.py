import csv
import chromadb
import os

# 1. 初始化資料庫連線
client = chromadb.PersistentClient(path="./chroma_db")

# 2. 定義 Collection 名稱
# 建議維持原名或統一名稱為 "fakenews_collection"
collection_name = "fake_news"

# 3. 🛡️ 關鍵步驟：清理舊資料
# 為了避免舊的 10 筆資料與新的 100 筆混在一起，我們先刪除舊的 collection 再重建
try:
    client.delete_collection(name=collection_name)
    print(f"🗑️ 已成功刪除舊的 collection: {collection_name}")
except Exception:
    print(f"ℹ️ 尚未存在既有 collection，將直接建立新的一個。")

# 4. 建立新的 Collection
collection = client.create_collection(name=collection_name)
print(f"🆕 已建立全新的 collection：{collection_name}")

# 5. 讀取新的 100 筆 Cofacts 資料
# 請確保檔名對應剛才產出的 clean_rumor_100.csv
new_csv_file = "clean_rumor_100.csv"

if not os.path.exists(new_csv_file):
    print(f"❌ 錯誤：找不到 {new_csv_file}，請確認檔案已在資料夾中。")
else:
    with open(new_csv_file, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        
        documents = []
        ids = []
        
        for i, row in enumerate(reader):
            # 新的 CSV 主要是 'text' 欄位
            text = row["text"]
            if text.strip(): # 確保不加入空字串
                documents.append(text)
                ids.append(f"rumor_{i}")

        # 6. 批次寫入資料庫 (效率較高)
        if documents:
            collection.add(
                documents=documents,
                ids=ids
            )
            print(f"✅ 成功將 {len(documents)} 筆真實假訊息寫入向量資料庫！")

print("📍 資料庫重建完成，路徑：./chroma_db")