from datasets import load_dataset
import pandas as pd

print("開始載入資料...")

# ⚠️ 只抓 1000 筆，不要全抓
dataset = load_dataset(
    "Cofacts/line-msg-fact-check-tw",
    "articles",
    split="train[:1000]"
)

print("轉成 DataFrame...")
df = pd.DataFrame(dataset)

print("過濾 RUMOR...")
df = df[df["status"] == "RUMOR"]

print("取前 100 筆...")
df = df.head(100)

print("只保留 text 欄位...")
df = df[["text"]]

print("儲存 CSV...")
df.to_csv("clean_rumor_100.csv", index=False)

print("✅ 完成 clean_rumor_100.csv")