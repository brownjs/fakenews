import pandas as pd
from huggingface_hub import hf_hub_download
import ssl
import csv
import sys

# 1. 繞過 SSL 驗證
ssl._create_default_https_context = ssl._create_unverified_context

# 2. 解決 C 引擎限制：手動調大欄位限制 (處理超大文本訊息)
csv.field_size_limit(sys.maxsize)

def main():
    print("🚀 啟動全量資料處理模式（解析引擎已優化）...")
    
    try:
        # 下載 articles.csv.zip
        print("📥 下載 articles.csv.zip...")
        articles_zip_path = hf_hub_download(
            repo_id="Cofacts/line-msg-fact-check-tw",
            filename="articles.csv.zip",
            repo_type="dataset",
            token=True
        )
        
        # 下載 article_replies.csv.zip
        print("📥 下載 article_replies.csv.zip...")
        rel_zip_path = hf_hub_download(
            repo_id="Cofacts/line-msg-fact-check-tw",
            filename="article_replies.csv.zip",
            repo_type="dataset",
            token=True
        )
        
        # 3. 讀取資料：改用 engine='python' 解決 Buffer Overflow
        print("📊 正在讀取並解析資料（使用 Python 引擎處理大容量文字）...")
        
        # articles 資料較大且內容複雜，需加強解析設定
        articles = pd.read_csv(
            articles_zip_path, 
            compression='zip', 
            engine='python',      # 核心修正：改用 Python 引擎
            on_bad_lines='warn',   # 遇到壞掉的行先跳過並警告，不中斷程式
            quoting=csv.QUOTE_MINIMAL 
        )
        
        relations = pd.read_csv(
            rel_zip_path, 
            compression='zip',
            engine='python'
        )
        
        print(f"✅ 讀取成功！原始文章: {len(articles)} 筆, 關聯標籤: {len(relations)} 筆")

        # 4. 過濾 RUMOR (假訊息)
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
        
        # 6. 去重並取全量
        all_rumors = merged_df[['text']].dropna().drop_duplicates()
        
        # 7. 輸出結果
        output_path = "all_rumors.csv"
        all_rumors.to_csv(output_path, index=False, encoding='utf-8-sig')
        
        print("-" * 30)
        print(f"🎉 處理完成！共產出 {len(all_rumors)} 筆真實假訊息。")
        print(f"📁 檔案已存至: {output_path}")
        print("-" * 30)

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")

if __name__ == "__main__":
    main()