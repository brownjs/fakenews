import pandas as pd
from huggingface_hub import hf_hub_download
import ssl

# Mac 必備 SSL 繞過
ssl._create_default_https_context = ssl._create_unverified_context

def main():
    print("🚀 修正檔名並重新執行 Cofacts 資料處理...")
    
    try:
        # 1. 下載 articles.csv.zip (注意多了 .zip)
        print("📥 下載 articles.csv.zip...")
        articles_zip_path = hf_hub_download(
            repo_id="Cofacts/line-msg-fact-check-tw",
            filename="articles.csv.zip",
            repo_type="dataset",
            token=True
        )
        
        # 2. 下載 article_replies.csv.zip
        print("📥 下載 article_replies.csv.zip...")
        rel_zip_path = hf_hub_download(
            repo_id="Cofacts/line-msg-fact-check-tw",
            filename="article_replies.csv.zip",
            repo_type="dataset",
            token=True
        )
        
        # 3. 讀取資料 (Pandas 的 compression='zip' 會自動處理)
        print("📊 正在解壓縮並讀取資料...")
        articles = pd.read_csv(articles_zip_path, compression='zip')
        relations = pd.read_csv(rel_zip_path, compression='zip')
        
        print(f"✅ 讀取成功！文章: {len(articles)} 筆, 關聯標籤: {len(relations)} 筆")

        # 4. 過濾判定為 RUMOR 的資料
        rumor_relations = relations[
            (relations['replyType'] == 'RUMOR') & 
            (relations['status'] == 'NORMAL')
        ]
        
        # 5. 合併 (Join)
        merged_df = pd.merge(
            rumor_relations[['articleId']], 
            articles[['id', 'text']], 
            left_on='articleId', 
            right_on='id'
        )
        
        # 6. 去重並取前 100 筆
        clean_rumor_1000 = merged_df[['text']].dropna().drop_duplicates().head(1000)
        
        # 7. 輸出結果
        output_path = "clean_rumor_1000.csv"
        clean_rumor_1000.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print("-" * 30)
        print(f"🎉 終於成功了！已產出: {output_path}")
        print(f"🔍 預覽內容：\n{clean_rumor_1000['text'].iloc[0][:50]}...")
        print("-" * 30)

    except Exception as e:
        print(f"❌ 依然發生錯誤: {e}")
        print("\n💡 如果看到 404，請確認 HF 頁面上的檔名是否確實為 articles.csv.zip")

if __name__ == "__main__":
    main()