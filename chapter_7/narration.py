from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip


def insert_audios_to_video(video_path, audio_info, output_path):
    # 動画ファイルを読み込む
    video = VideoFileClip(video_path)

    # 元の動画に音声がある場合、それも保持したいなら抽出しておく
    # 不要（完全に差し替え）なら元の音声は無視してOK
    original_audio = video.audio

    # 挿入する音声クリップのリストを作成
    audio_clips = []

    # 元の音声を残す場合はリストに追加
    if original_audio is not None:
        audio_clips.append(original_audio)

    for path, start_time in audio_info:
        # 音声ファイルを読み込み、開始時間をセット
        a_clip = AudioFileClip(path).with_start(start_time)
        audio_clips.append(a_clip)

    # すべての音声を重ね合わせる (CompositeAudioClip)
    # これにより、指定した時間にそれぞれの音声が流れるようになる
    final_audio = CompositeAudioClip(audio_clips)

    # 動画に新しい音声をセット
    final_video = video.with_audio(final_audio)

    # 書き出し (動画コーデックと音声コーデックを指定)
    # mov形式を維持する場合、libx264などが一般的
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")


# --- 実行例 ---
target_video = "sample_data/sample_narration.mov"
audio_list = [
    ("sample_data/line1.wav", 0),  # 0秒地点から再生
    ("sample_data/line2.wav", 3),  # 3秒地点から再生
    ("sample_data/line3.wav", 6),  # 6秒地点から再生
    ("sample_data/line4.wav", 9),  # 9秒地点から再生
]

output_file = "output_narration.mov"
insert_audios_to_video(target_video, audio_list, output_file)
