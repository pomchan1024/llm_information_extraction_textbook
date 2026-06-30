import pandas as pd
from collections import Counter

# 単語の出現回数を集計
word_freq = Counter(words)

# Pandasのデータフレームに変換
df = pd.DataFrame(word_freq.items(), columns=["単語", "出現回数"])

# 出現回数が多い順にソート
df_sorted = df.sort_values(by="出現回数", ascending=False)

print(df_sorted.head(5))