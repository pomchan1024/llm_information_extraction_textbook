! pip install janome==0.5.0

from janome.tokenizer import Tokenizer

# ファイルの読み込み
with open("study.txt", mode="r", encoding="utf-8") as f:
    text = f.read()

# 形態素解析の実行
t = Tokenizer()
# 各単語をリストに抽出
words = [token.surface for token in t.tokenize(text)]

# 結果の表示
print(f"全単語リスト: {words}")