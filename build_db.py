import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from tqdm import tqdm

# 使用多語言 Embedding 模型（支援中文）
multilingual_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="paraphrase-multilingual-MiniLM-L12-v2"
)

# 建立新的 collection，指定中文 Embedding 模型
client = chromadb.PersistentClient(path="./chroma_db")

# 先刪除舊的 collection，重新建立
try:
    client.delete_collection(name="fake_news")
    print("🗑️ 舊資料庫已清除")
except:
    pass

collection = client.get_or_create_collection(
    name="fake_news",
    embedding_function=multilingual_ef
)

def build_huge_db():
    df = pd.read_csv("all_rumors.csv")
    documents = df['text'].dropna().tolist()
    ids = [f"id_{i}" for i in range(len(documents))]
    
    batch_size = 500  # 換模型後每批改小一點，比較穩
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