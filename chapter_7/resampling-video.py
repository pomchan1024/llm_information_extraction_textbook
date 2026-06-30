! pip install ffmpeg-python==0.2.0

import ffmpeg

def resample_for_gemini(input_file, output_file):
    # 動画ストリームの入力
    stream = ffmpeg.input(input_file)

    # 映像処理: 1fps、横幅640px
    video = stream.video.filter('fps', fps=1).filter('scale', 640, -1)

    # 音声処理: 16kHzにサンプリングレートを変更
    # モノラル化は output 側で行うため、ここではリサンプルのみ
    audio = stream.audio.filter('aresample', 16000)

    # 出力設定
    out = ffmpeg.output(
        video, audio, output_file,
        vcodec='libx264',
        acodec='aac',
        ac=1,              # ここでオーディオチャンネルを1（モノラル）に指定
        pix_fmt='yuv420p',  # iPhone動画の変換で推奨されるピクセルフォーマット
        strict='experimental'
    )

    try:
        # 実行
        out.run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
        print(f"変換が完了しました。保存先: {output_file}")
    except ffmpeg.Error as e:
        print("=== FFmpeg Error Message ===")
        # エラーが発生した場合は詳細を出力
        print(e.stderr.decode())

# 実行例
input_video = "sample_data/sample.mov"
output_video = "output.mp4"

resample_for_gemini(input_video, output_video)