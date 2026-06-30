def fixed_size_chunking(text, chunk_size, overlap_size):
    chunks = []
    start = 0

    while start < len(text):
        # 指定したサイズで切り出し
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)

        # 次の開始位置を計算 (サイズ - オーバーラップ分だけ進む)
        start += (chunk_size - overlap_size)

        # 残りの文字数が少なすぎる場合にループを抜ける
        if start >= len(text):
            break

    return chunks


# --- 実行例 ---
text = """抽出されたデータを保存するデータベースのアクセス権限も、入力元のドキュメントと同等、あるいはそれ以上に厳格に管理されるべきです。「元の PDF ファイルは削除したけれど、抽出後の JSON データはいつまでもデータベースに残っている」という状態は、情報のライフサイクル管理の観点から望ましくありません。情報の抽出が完了し、目的を果たしたデータについては、あらかじめ定められた保管期間が過ぎたら、速やかに消去する仕組みを整えておくことが、システム全体の安全性を高めることにつながります。"""

# 実行
chunks = fixed_size_chunking(text, chunk_size=30, overlap_size=10)

for i, chunk in enumerate(chunks):
    print(f"Chunk {i + 1}: {repr(chunk)}")