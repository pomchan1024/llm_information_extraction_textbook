import cv2


def draw_bboxes_with_labels(image_path, bboxes, output_path):
    """
    bboxes: [[xmin, ymin, xmax, ymax], ...] のリスト
    """
    # 画像の読み込み
    img = cv2.imread(image_path)

    # 描画設定
    line_color = (0, 255, 0)  # 緑色の枠
    line_thickness = 2
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 2

    for i, bbox in enumerate(bboxes):
        xmin, ymin, xmax, ymax = map(int, bbox)

        # バウンディングボックスの描画
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), line_color, line_thickness)

        # ラベル用の黒い正方形のサイズを計算
        label = str(i + 1)
        # 書き込むための文字のサイズや位置を取得
        (text_w, text_h), baseline = \
            cv2.getTextSize(label, font, font_scale, font_thickness)

        # 正方形のサイズ（文字の幅・高さの大きい方に合わせる + 余白）
        square_size = max(text_w, text_h) + 10

        # 黒い正方形の座標 (左上の頂点)
        sq_x1, sq_y1 = xmin, ymin - square_size
        sq_x2, sq_y2 = xmin + square_size, ymin

        # 画像の外にはみ出さないための処理（yminが小さい場合）
        if sq_y1 < 0:
            sq_y1, sq_y2 = ymin, ymin + square_size

        # 黒い正方形を描画 (背景)
        cv2.rectangle(img, (sq_x1, sq_y1), (sq_x2, sq_y2), (0, 0, 0), -1)

        # 白い文字を描画
        # 文字が正方形の中央に来るように調整
        # batch-image-generation.pyでは手動で位置調整したが、ここでは自動で調整する
        text_x = sq_x1 + (square_size - text_w) // 2
        text_y = sq_y1 + (square_size + text_h) // 2
        cv2.putText(img, label, (text_x, text_y), font, font_scale, \
                    (255, 255, 255), font_thickness)

    # 保存と表示
    cv2.imwrite(output_path, img)
    print(f"保存完了: {output_path}")


# --- 実行例 ---
sample_image = "sample_data/sample_photo2.jpg"
# バウンディングボックスの座標を入力
# 今回は手動で座標値を設定したが、物体検出で得られたバウンディングボックスの座標値を入力しても良い
sample_bboxes = [
    [40, 150, 350, 450],
    [450, 350, 650, 540],
]  # [xmin, ymin, xmax, ymax] の形式

draw_bboxes_with_labels(sample_image, sample_bboxes, "boxed_image.jpg")
