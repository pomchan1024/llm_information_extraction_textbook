import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt


def generate_clip_gradcam(image_path, text_query):
    # モデルとプロセッサの準備
    model_id = "openai/clip-vit-base-patch32"
    # gpuの使用設定、デフォルトではcpuを使用する
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = CLIPModel.from_pretrained(model_id).to(device)
    processor = CLIPProcessor.from_pretrained(model_id)

    # 入力の準備
    image = Image.open(image_path).convert("RGB")
    inputs = processor(text=[text_query], images=image, \
                       return_tensors="pt", padding=True).to(device)

    # 勾配と活性化値を取得するための設定
    # CLIPのVisionエンコーダの最終層のLayerNormをターゲットにする
    target_layer = model.vision_model.encoder.layers[-1].layer_norm1

    activations = []
    gradients = []

    def forward_hook(module, input, output):
        activations.append(output)

    def backward_hook(module, grad_input, grad_output):
        gradients.append(grad_output[0])

    # フック(モデル内部に独自の処理を割り込ませて実行する)を設定
    h1 = target_layer.register_forward_hook(forward_hook)
    h2 = target_layer.register_full_backward_hook(backward_hook)

    # 推論と勾配計算
    # logits_per_image は (batch, text_input_size) の形状
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image

    model.zero_grad()
    logits_per_image.backward()

    # フックの解除
    h1.remove()
    h2.remove()

    # Grad-CAMの計算
    # 最終層の勾配(gradients)と活性化(activations)から重みを算出
    grads = gradients[0]  # (1, 50, 768)の3次元配列
    acts = activations[0]  # (1, 50, 768)の3次元配列

    # パッチごとの重要度を計算
    weights = torch.mean(grads, dim=1, keepdim=True)
    cam = torch.sum(weights * acts, dim=-1)  # (1, 50)の2次元配列

    # [CLS]トークン（先頭）を除いた残り49個(7x7)のタイル画像(パッチ)を読み込む
    cam = cam[0, 1:].detach().cpu().numpy()

    # ヒートマップの生成
    grid_size = int(np.sqrt(cam.shape[0]))
    mask = cam.reshape(grid_size, grid_size)

    # ReLU処理（正の寄与のみ）と正規化
    mask = np.maximum(mask, 0)
    mask = (mask - mask.min()) / (mask.max() - mask.min() + 1e-8)

    # 可視化
    original_img = np.array(image)
    mask_resized = cv2.resize(mask, (original_img.shape[1], original_img.shape[0]))

    heatmap = cv2.applyColorMap(np.uint8(255 * mask_resized), cv2.COLORMAP_JET)
    heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)

    overlay = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)

    # 表示
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(original_img)
    plt.title(f"Query: {text_query}")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(overlay)
    plt.title("Grad-CAM (Text-guided)")
    plt.axis('off')
    plt.show()


# --- 実行例 ---
generate_clip_gradcam("sample_data/sample_photo1.jpg", "cat")