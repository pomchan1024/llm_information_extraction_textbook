from PIL import Image, ImageDraw, ImageFont


def create_combined_image(image_paths, output_path, target_height=500, spacing=20):
    processed_images = []
    total_width = 0

    # フォントの設定（環境に合わせてパスを変更する）
    try:
        font = ImageFont.truetype("LiberationSans-Regular.ttf", 35)
    except:
        font = ImageFont.load_default()

    for i, path in enumerate(image_paths):
        with Image.open(path) as img:
            # アスペクト比を維持して各画像をリサイズ
            aspect_ratio = img.width / img.height
            new_width = int(target_height * aspect_ratio)
            img_resized = img.resize((new_width, target_height), \
                                     Image.Resampling.LANCZOS)

            # 番号ラベル（黒い正方形に白文字）の作成
            draw = ImageDraw.Draw(img_resized)
            label_size = 40  # 正方形のサイズ
            label_margin = 10  # 端からの距離

            # 黒い正方形を描画
            rect_coords = [label_margin, label_margin, label_margin + label_size, \
                           label_margin + label_size]
            draw.rectangle(rect_coords, fill="black")

            # 白い文字を描画 (中央付近に配置)
            text = str(i + 1)
            draw.text((label_margin + 9, label_margin + 0), text, \
                      fill="white", font=font)

            processed_images.append(img_resized)
            total_width += new_width

    # 連結用のキャンバス作成（背景は白）
    canvas_width = total_width + (spacing * (len(processed_images) - 1))
    combined_img = Image.new('RGB', (canvas_width, target_height), (255, 255, 255))

    # 画像を順に貼り付け
    current_x = 0
    for img in processed_images:
        combined_img.paste(img, (current_x, 0))
        current_x += img.width + spacing

    # 保存
    combined_img.save(output_path)
    print(f"保存完了: {output_path}")


# --- 実行例 ---
image_files = ["sample_data/sample_photo1.jpg", "sample_data/sample_photo2.jpg", \
               "sample_data/sample_photo3.jpg"]
create_combined_image(image_files, "combined_result.jpg")