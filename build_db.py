import csv
import chromadb

# 用 PersistentClient 才會真的把資料存到本地資料夾
client = chromadb.PersistentClient(path="./chroma_db")

# 如果 collection 已存在，可以直接拿來用
collection_name = "fake_news"

# 先檢查目前有哪些 collections
existing_collections = client.list_collections()
existing_names = [c.name for c in existing_collections]

if collection_name in existing_names:
    collection = client.get_collection(name=collection_name)
    print(f"已找到既有 collection：{collection_name}")
else:
    collection = client.create_collection(name=collection_name)
    print(f"已建立新 collection：{collection_name}")

# 讀取 sample_data.csv
with open("sample_data.csv", "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for i, row in enumerate(reader):
        text = row["text"]
        label = row["label"]

        # 加入資料
        collection.add(
            documents=[text],
            metadatas=[{"label": label}],
            ids=[str(i)]
        )

print("✅ 10 筆資料已成功寫入 Chroma！")