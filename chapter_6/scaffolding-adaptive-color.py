import cv2
import numpy as np


def draw_grid_points(image_path, output_path, rows=6, cols=6):
    # 画像の読み込み
    img = cv2.imread(image_path)

    h, w = img.shape[:2]

    # 格子点の間隔を計算
    start_x, end_x = int(w * 0.1), int(w * 0.9)
    start_y, end_y = int(h * 0.1), int(h * 0.9)

    y_coords = np.linspace(start_y, end_y, rows, dtype=int)
    x_coords = np.linspace(start_x, end_x, cols, dtype=int)

    for i, y in enumerate(y_coords):
        for j, x in enumerate(x_coords):
            # --- ここから背景色適応ロジック ---
            # 点の周囲（10x10ピクセル）の平均色を取得
            roi = img[max(0, y - 5):min(h, y + 5), max(0, x - 5):min(w, x + 5)]
            avg_color = np.mean(roi, axis=(0, 1))  # BGRの平均

            # 輝度(Luminance)を計算 (OpenCVはBGR順なので注意)
            brightness = 0.114 * avg_color[0] + 0.587 * avg_color[1] \
                         + 0.299 * avg_color[2]

            # 背景が明るければ黒(0,0,0)、暗ければ白(255,255,255)を選択
            color = (0, 0, 0) if brightness > 128 else (255, 255, 255)
            # --- ここまで ---

            # 座標ラベル (行, 列) ※1始まり
            label = f"({i + 1},{j + 1})"

            # 格子点を描画
            cv2.circle(img, (x, y), 5, color, -1)

            # 座標テキストを描画
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2

            text_pos = (x + 10, y + 10)
            cv2.putText(img, label, text_pos, font, font_scale, color, \
                        thickness, cv2.LINE_AA)

    # 結果を保存
    cv2.imwrite(output_path, img)
    print(f"保存完了: {output_path}")


# --- 実行例 ---
draw_grid_points('sample_data/sample_photo2.jpg', 'grid_image.jpg')