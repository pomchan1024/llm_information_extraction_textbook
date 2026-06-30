! pip install moviepy==2.2.1

from moviepy import VideoFileClip
import os


def video_fixed_length_chunking(file_path, output_dir, chunk_length_sec=30, \
    overlap_sec=5):
    # 出力ディレクトリの作成（複数の分割動画データを格納するためのフォルダ）
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 動画ファイルの読み込み
    video = VideoFileClip(file_path)
    total_sec = video.duration

    # 分割のステップ（長さ - オーバーラップ）
    step_sec = chunk_length_sec - overlap_sec

    chunk_paths = []
    start_sec = 0

    while start_sec < total_sec:
        end_sec = start_sec + chunk_length_sec

        # 最終チャンクが動画時間を超えないように調整
        actual_end_sec = min(end_sec, total_sec)

        # 指定範囲を切り出し
        # subclip(開始秒, 終了秒)
        chunk = video.subclipped(start_sec, actual_end_sec)

        # ファイル名の作成
        chunk_name = f"chunk_{int(start_sec)}s_to_{int(actual_end_sec)}s.mp4"
        chunk_path = os.path.join(output_dir, chunk_name)

        # 書き出し（音声も自動的に含まれる）
        # codecを指定することで互換性を高める
        chunk.write_videofile(chunk_path, codec="libx264", audio_codec="aac")

        chunk_paths.append(chunk_path)

        # 次の開始位置へ（ステップ分進める）
        start_sec += step_sec

        # 終了判定
        if end_sec >= total_sec:
            break

    # メモリ解放
    video.close()
    return chunk_paths


# --- 実行例 ---
file_path = "sample_data/sample.mov"
output_dir="video_chunks"
chunk_paths = video_fixed_length_chunking(file_path, output_dir, \
    chunk_length_sec=4, overlap_sec=1)