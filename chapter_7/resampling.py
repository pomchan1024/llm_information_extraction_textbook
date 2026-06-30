! pip install librosa==0.11.0

import librosa

# 元のレートにかかわらずsr=16000に変換して読み込む
voice_path = "sample_data/sample_audio_8khz.wav"
y, sr = librosa.load(voice_path, sr=16000)