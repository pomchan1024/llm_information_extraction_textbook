!pip
install
inaSpeechSegmenter == 0.7
.7

from inaSpeechSegmenter import Segmenter
import pandas as pd

# セグメンターの初期化
# gender_detected=True にすると男女の判別も行う
seg = Segmenter(vad_engine='smn', detect_gender=True)

# 音声ファイルの解析
# 戻り値は (ラベル, 開始時間, 終了時間) のリスト
input_file = 'sample_voice.wav.wav'
segmentation = seg(input_file)

# 結果の表示とフィルタリング
print(f"--- 解析結果: {input_file} ---")
speech_segments = []

for label, start, end in segmentation:
    print(f"Label: {label:10} | Start: {start:7.2f}s | End: {end:7.2f}s")

    # 'male' または 'female' （音声区間）だけをピックアップ
    if label in ['male', 'female']:
        speech_segments.append({'start': start, 'end': end, 'label': label})

df = pd.DataFrame(speech_segments)
print("\n--- 抽出された発話区間 ---")
print(df)