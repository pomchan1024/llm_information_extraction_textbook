! pip install webrtcvad-wheels
! pip install pydub==0.25.1

import webrtcvad
from pydub import AudioSegment


def get_speech_segments(file_path, aggressiveness=1):
    # 前処理: webrtcvadが受け取れる形式（16kHz/モノラル）に変換
    sample_rate = 16000
    audio = AudioSegment.from_file(file_path).set_frame_rate(sample_rate) \
        .set_channels(1).set_sample_width(2)

    # VADの初期化
    vad = webrtcvad.Vad(aggressiveness)

    # 30msごとのフレームに分割して判定
    frame_duration_ms = 30
    frame_size = int(sample_rate * frame_duration_ms / 1000) * 2  # bytes
    raw_data = audio.raw_data

    segments = []
    is_speech_active = False
    start_time = 0

    for i in range(0, len(raw_data), frame_size):
        frame = raw_data[i:i + frame_size]
        if len(frame) < frame_size: break

        current_time = (i / len(raw_data)) * (len(audio) / 1000.0)
        is_speech = vad.is_speech(frame, sample_rate)

        # 状態の変化（無音→発話、発話→無音）を検知し、フラグを更新
        if is_speech and not is_speech_active:
            is_speech_active = True
            start_time = current_time
        elif not is_speech and is_speech_active:
            is_speech_active = False
            segments.append({'label': 'speech', 'start': start_time, \
                             'end': current_time})

    # ファイル末尾が発話中だった場合、最後に強制的に発話終了とする
    if is_speech_active:
        segments.append({'label': 'speech', 'start': start_time, \
                         'end': len(audio) / 1000.0})

    return segments


# --- 実行例 ---
input_file = 'sample_data/sample_stereo_44khz.wav'
speech_segments = get_speech_segments(input_file, aggressiveness=2)

# 音声の読み込みと結合処理
original_audio = AudioSegment.from_file(input_file).set_frame_rate(16000).set_channels(1)
combined = AudioSegment.empty()
silence_gap = AudioSegment.silent(duration=100)

for seg in speech_segments:
    start_ms = seg['start'] * 1000
    end_ms = seg['end'] * 1000
    combined += original_audio[start_ms:end_ms] + silence_gap

# 書き出し
combined.export("output_vad.wav", format="wav")

