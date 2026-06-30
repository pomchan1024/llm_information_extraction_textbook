import librosa
import noisereduce as nr
import soundfile as sf
import torch
from speechbrain.inference.enhancement import SpectralMaskEnhancement


def clean_audio(input_path, output_path):
    # 読み込み (16kHz, モノラル)
    y, sr = librosa.load(input_path, sr=44100, mono=True)

    # 残響除去 (Dereverberation)
    # SpeechBrainの学習済みモデルを使用
    enhance_model = SpectralMaskEnhancement.from_hparams(
        source="speechbrain/metricgan-plus-voicebank",
        savedir="pretrained_models/metricgan-plus-voicebank"
    )

    # データをモデルの形式に変換して実行
    y_tensor = torch.FloatTensor(y).unsqueeze(0)
    enhanced = enhance_model.enhance_batch(y_tensor, lengths=torch.tensor([1.0]))
    y_processed = enhanced.cpu().detach().numpy().flatten()

    # ノイズ除去 (Noise Reduction)
    # 残響除去後に残った微細な背景雑音をカット
    y_final = nr.reduce_noise(y=y_processed, sr=sr, prop_decrease=0.8)

    # 保存
    sf.write(output_path, y_final, sr)
    print(f"処理完了: {output_path}")


# --- 実行例 ---
clean_audio("sample_data/sample_stereo_44khz.wav", "cleaned_audio.wav")