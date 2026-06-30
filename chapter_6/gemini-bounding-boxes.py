import cv2

def draw_scaled_bounding_boxes(image_path, detections):

    # 画像の寸法を取得
    image = cv2.imread(image_path)
    h_img, w_img = image.shape[:2]

    # 描画用に画像をコピー（元の画像を変更しないため）
    output_image = image.copy()

    # Gemini >= 2.0のスケール基準値
    SCALE_BASE = 1000.0

    # 描画設定 (色: 緑, 線の太さ: 2)
    box_color = (0, 255, 0)
    thickness = 2

    for box in detections:
        # 入力形式: [ymin, xmin, ymax, xmax] (0-1000スケール)
        ymin_rel, xmin_rel, ymax_rel, xmax_rel = box

        # 座標変換処理
        # 相対座標(0-1000) を 絶対ピクセル座標 に変換します。
        # 計算式: (相対座標 / 1000.0) * 画像の実際の寸法
        # ピクセル座標なので int型に変換します。

        xmin_abs = int((xmin_rel / SCALE_BASE) * w_img)
        ymin_abs = int((ymin_rel / SCALE_BASE) * h_img)
        xmax_abs = int((xmax_rel / SCALE_BASE) * w_img)
        ymax_abs = int((ymax_rel / SCALE_BASE) * h_img)

        # 座標が画像の範囲外に出ないようにクリップする
        xmin_abs = max(0, min(xmin_abs, w_img - 1))
        ymin_abs = max(0, min(ymin_abs, h_img - 1))
        xmax_abs = max(0, min(xmax_abs, w_img - 1))
        ymax_abs = max(0, min(ymax_abs, h_img - 1))

        # 描画処理
        # cv2.rectangle は 引数に (x座標, y座標) の順序でタプルを受け取ります。
        # 左上の点 (xmin, ymin) と 右下の点 (xmax, ymax) を指定します。
        cv2.rectangle(
            output_image,
            (xmin_abs, ymin_abs),
            (xmax_abs, ymax_abs),
            box_color,
            thickness
        )

    return output_image

# --- 実行例 ---
image_file = "sample_data/sample_bounding_box.jpg"

# 物体検出結果 ([ymin, xmin, ymax, xmax], 0-1000スケール)
detections = [
    [631, 95, 989, 369],
    [432, 244, 922, 675]
    ]

# 関数を呼び出して描画
result_image = draw_scaled_bounding_boxes(image_file, detections)

# 結果を保存
cv2.imwrite("output_bounding_box.jpg", result_image)