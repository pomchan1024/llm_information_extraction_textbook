import cv2
import numpy as np


def draw_grid_points(image_path, output_path, rows=6, cols=6):
    # 画像の読み込み
    img = cv2.imread(image_path)

    h, w = img.shape[:2]

    # 格子点の間隔を計算
    # 画像の端に寄りすぎないよう、10%〜90%の範囲に配置する
    start_x, end_x = int(w * 0.1), int(w * 0.9)
    start_y, end_y = int(h * 0.1), int(h * 0.9)

    y_coords = np.linspace(start_y, end_y, rows, dtype=int)
    x_coords = np.linspace(start_x, end_x, cols, dtype=int)

    # 赤色の設定 (BGR形式なので 赤は (0, 0, 255))
    color = (0, 0, 255)

    for i, y in enumerate(y_coords):
        for j, x in enumerate(x_coords):
            # 座標ラベル (行, 列) ※1始まり
            label = f"({i + 1},{j + 1})"

            # 格子点を描画
            cv2.circle(img, (x, y), 5, color, -1)  # 半径5の塗りつぶし円

            # 座標テキストを描画
            # フォント、スケール、太さを調整
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 2

            # テキストを点の少し右下に配置
            text_pos = (x + 10, y + 10)
            cv2.putText(img, label, text_pos, font, font_scale, color, \
                        thickness, cv2.LINE_AA)

    # 結果を保存
    cv2.imwrite(output_path, img)
    print(f"保存完了: {output_path}")


# --- 実行例 ---
draw_grid_points('sample_data/sample_photo2.jpg', 'grid_image.jpg')