! pip install pydub==0.25.1

from pydub import AudioSegment
import os


def fixed_length_chunking(file_path, chunk_length_sec=30, overlap_sec=5, \
                          output_dir="chunks"):
    # 出力ディレクトリの作成（複数の分割音声データを格納するためのフォルダ）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 音声ファイルの読み込み
    audio = AudioSegment.from_file(file_path)

    # ミリ秒単位に変換
    chunk_length_ms = chunk_length_sec * 1000
    overlap_ms = overlap_sec * 1000
    total_ms = len(audio)

    # 分割のステップ（長さ - オーバーラップ）
    step_ms = chunk_length_ms - overlap_ms

    # チャンキング処理
    chunks = []
    for start_ms in range(0, total_ms, step_ms):
        end_ms = start_ms + chunk_length_ms
        chunk = audio[start_ms:end_ms]

        # チャンクの保存
        chunk_name = f"chunk_{start_ms // 1000}s_to_{min(end_ms, total_ms) // 1000}s.wav"
        chunk_path = os.path.join(output_dir, chunk_name)
        chunk.export(chunk_path, format="wav")

        chunks.append(chunk_path)

        # 終端に達したら終了
        if end_ms >= total_ms:
            break

    return chunks


# --- 実行例 ---
chunk_paths = fixed_length_chunking("sample_data/sample_stereo_44khz.wav", chunk_length_sec=4, \
                                    overlap_sec=1)
print(f"分割完了: {len(chunk_paths)} 個のファイルを作成しました。")