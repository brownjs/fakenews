import pandas as pd
import chromadb
from tqdm import tqdm # 建議安裝 pip install tqdm 來跑進度條

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="fake_news")

def build_huge_db():
    df = pd.read_csv("all_rumors.csv")
    documents = df['text'].dropna().tolist()
    ids = [f"id_{i}" for i in range(len(documents))]
    
    batch_size = 1000 # 每次只處理 1000 筆
    print(f"🚀 開始批次處理 {len(documents)} 筆資料...")
    
    for i in tqdm(range(0, len(documents), batch_size)):
        batch_docs = documents[i : i + batch_size]
        batch_ids = ids[i : i + batch_size]
        
        collection.add(
            documents=batch_docs,
            ids=batch_ids
        )
    
    print("✅ 全量資料庫建置完成！")

if __name__ == "__main__":
    build_huge_db()