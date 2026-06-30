import re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

# フォントの準備
! apt-get install -y fonts-noto-cjk
font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def create_text_image(text, font_path, font_size=40, color=(255, 255, 0), \
                      stroke_color=(0, 0, 0)):
    font = ImageFont.truetype(font_path, font_size)
    # テキストの範囲を計算
    bbox = font.getbbox(text)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    # 余裕を持たせた寸法のキャンバスを用意
    img = Image.new('RGBA', (w + 40, h + 40), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 縁取り付きで描画
    draw.text((20, 20), text, font=font, fill=color,
              stroke_width=2, stroke_fill=stroke_color)
    return np.array(img)


def add_subtitles_colab(video_path, gemini_text, font_path, \
                        output_path="final_video.mp4"):
    # Gemini出力をパース
    pattern = r"\[(\d{2}):(\d{2}) - (\d{2}):(\d{2})\]\s*(.*)"
    lines = gemini_text.strip().split('\n')

    video = VideoFileClip(video_path)
    clips = [video]

    for line in lines:
        match = re.match(pattern, line)
        if match:
            s_m, s_s, e_m, e_s, content = match.groups()
            start_t = int(s_m) * 60 + int(s_s)
            end_t = int(e_m) * 60 + int(e_s)
            clean_text = content.split('：')[-1].replace("**", "")

            # Pillowで画像化
            text_array = create_text_image(clean_text, font_path)

            # MoviePyのImageClipとして重ねる
            txt_clip = (ImageClip(text_array)
                        .with_start(start_t)
                        .with_end(end_t)
                        .with_duration(end_t - start_t)
                        .with_position(('center', video.h * 0.8)))
            clips.append(txt_clip)

    final = CompositeVideoClip(clips)
    final.write_videofile(output_path, codec="libx264", audio_codec="aac", \
                          fps=video.fps)
    video.close()


# --- 実行例 ---
video_path = "sample_data/sample.mov"
gemini_output = """
[00:02 - 00:04] ホクトくん。
[00:04 - 00:06] 何食べたいですか？
[00:08 - 00:09] いらない？
"""

add_subtitles_colab(video_path, gemini_output, font_path)