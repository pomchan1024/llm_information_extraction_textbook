from PIL import Image
import numpy as np

# 100x100の白い画像を作成して保存
white_img = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 255)
white_img.save("sample.png")

# 画像の読み込み
img = Image.open("sample.png")
print(f"寸法: {img.size}, 形式: {img.format}")

# リサイズと保存
img_small = img.resize((50, 50))
img_small.save("sample_small.png")