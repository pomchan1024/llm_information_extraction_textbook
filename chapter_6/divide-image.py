import cv2
import numpy as np
import os


def split_image_with_overlap(image_path, a, b, c, d, output_dir="output"):
    # 画像の読み込み
    img = cv2.imread(image_path)
    if img is None:
        print("画像が見つかりません。")
        return

    h, w, _ = img.shape
    os.makedirs(output_dir, exist_ok=True)

    # 最終的な1パーツの寸法
    target_w = a + 2 * c
    target_h = b + 2 * d

    # 端の部分で「のりしろ」が足りなくなるのを防ぐため、あらかじめ画像をパディング
    # 上下左右にc, dのピクセル分、鏡像（Reflect）で埋める
    padded_img = cv2.copyMakeBorder(img, d, d, c, c, cv2.BORDER_REFLECT)

    count = 0
    # 元の画像の座標(y, x)を基準に、a, bの間隔でループを回す
    for y in range(0, h, b):
        for x in range(0, w, a):
            # padded_img上での切り出し開始位置
            # (y, x)はpadded_img内では (y+d, x+c) に相当する
            start_y = y
            start_x = x

            # 切り出し
            tile = padded_img[start_y: start_y + target_h, \
                   start_x: start_x + target_w]

            # 保存
            save_path = os.path.join(output_dir, f"tile_{count}_{y}_{x}.jpg")
            cv2.imwrite(save_path, tile)
            count += 1

    print(f"分割完了: {count}個の画像を '{output_dir}' に保存しました。")


# --- 実行例 ---
image_file = "sample_data/sample_divide.jpg"
a_size, b_size = 480, 320  # 基本寸法 (横, 縦)
c_margin, d_margin = 48, 32  # オーバーラップ幅 (横, 縦)

split_image_with_overlap(image_file, a_size, b_size, c_margin, d_margin)