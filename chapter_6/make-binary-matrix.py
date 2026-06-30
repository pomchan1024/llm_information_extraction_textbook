import cv2
import numpy as np

def image_to_binary_array_with_resize(original_image_path, llm_image_path):
    # 解析対象の画像をグレースケールで読み込み
    target_gray = cv2.imread(llm_image_path, cv2.IMREAD_GRAYSCALE)
    # 寸法の基準となる画像を読み込み
    base_img = cv2.imread(original_image_path)


    # 画像の寸法を取得
    h, w = base_img.shape[:2]

    # ターゲット画像を基準寸法にリサイズ
    # INTER_NEAREST を使うことで、補完によって0.5のような中間値が出るのを防ぎます
    resized_gray = cv2.resize(target_gray, (w, h), interpolation=cv2.INTER_NEAREST)

    # 255の半分（127）を基準に二値化 (0 or 1)
    _, binary_img = cv2.threshold(resized_gray, 127, 1, cv2.THRESH_BINARY)

    # リスト形式に変換して返す
    return binary_img.tolist()


# --- 実行例 ---
image_file = "sample_data/sample_bounding_box.jpg"
mask_file = "sample_data/sample_mask.jpg"

result = image_to_binary_array_with_resize(image_file, mask_file)
result_array = np.array(result, dtype=np.uint8)
# カンマ区切りのCSVとして保存
np.savetxt("binary_matrix.csv", result_array, fmt='%d', delimiter=',')

