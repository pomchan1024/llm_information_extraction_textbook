import cv2

# 画像を読み込み (OpenCVはBGR形式で読み込む)
img_cv = cv2.imread("sample.png")

# 1. グレースケール変換 (カラー情報を輝度のみにする)
gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
cv2.imwrite("gray.png", gray)

# 2. ぼかし処理 (ガウシアンフィルタ)
# (5, 5)はカーネルサイズと呼ばれ、大きいほど強くぼける
blur = cv2.GaussianBlur(img_cv, (5, 5), 0)
cv2.imwrite("blur.png", blur)

# 3. エッジ検出 (Canny法)
# 画像内の急激な色の変化を線として抽出する
edges = cv2.Canny(gray, 100, 200)
cv2.imwrite("edges.png", edges)