! pip install janome==0.5.0

import re
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

# Tokenizerを初期化
t = Tokenizer()


# 形態素解析（分かち書き）用の関数
def tokenize_jp(text):
    # 抽出する品詞を指定
    target_postypes = ["名詞", "動詞", "形容詞"]

    tokens = []
    for token in t.tokenize(text):
        # 品詞の第一節を取得
        pos = token.part_of_speech.split(',')[0]
        if pos in target_postypes:
            # 原形（base_form）を使うことで、活用語も統一してカウントできる
            # base_formが取得できない（'*' の）場合は表層形を使用する
            word = token.base_form if token.base_form != '*' else token.surface
            tokens.append(word)

    return " ".join(tokens)


# 重要単語抽出メインロジック
def extract_keywords_with_tfidf(raw_docs, top_n=5):
    # 1文ずつ形態素解析を実行
    tokenized_docs = [tokenize_jp(doc) for doc in raw_docs]

    # TF-IDF ベクトライザの設定
    vectorizer = TfidfVectorizer(use_idf=True)
    tfidf_matrix = vectorizer.fit_transform(tokenized_docs)
    terms = vectorizer.get_feature_names_out()

    results = []
    for i in range(len(raw_docs)):
        # 全文書のスコアが詰まった行列から各文のデータを取得しベクトル化
        doc_vector = tfidf_matrix.getrow(i).toarray().flatten()
        # 高いスコアのトークンを検索
        top_indices = doc_vector.argsort()[::-1][:top_n]

        important_words = [
            (terms[idx], round(doc_vector[idx], 4))
            for idx in top_indices if doc_vector[idx] > 0
        ]
        results.append(important_words)

    return results


# --- 実行例 ---
sample_texts = [
    "また、欲しい情報が何らかの理由で完全に欠損してしまっている、と言うこともしばしば起こります。特に、レシートは合計金額やお釣りが最下部に記載されることが多く、写真を撮る際に見切れてしまいやすいです。",
    "バウンディングボックスの左上の隅には、番号を示す記号を記載してください。記号は、黒い正方形に、白地で番号が記載されたものとします。",
    "LLMは欠損が生じた場合でも、その周辺情報から自発的に補完しようとする場合があることが分かりました。"
]

keywords = extract_keywords_with_tfidf(sample_texts, top_n=3)

for i, words in enumerate(keywords):
    print(f"文書 {i + 1} の重要単語:")
    print(words)