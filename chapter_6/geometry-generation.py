import matplotlib.pyplot as plt

def draw_square_with_line():
    # 正方形の頂点の座標を設定 (1辺の長さを3とします)
    # A(0, 3), B(0, 0), C(3, 0), D(3, 3)
    A = [0, 3]
    B = [0, 0]
    C = [3, 0]
    D = [3, 3]

    # 点M (辺ABの中点)
    # AとBの平均: (0+0)/2, (3+0)/2
    M = [0, 1.5]

    # 点N (辺CDを1:2に内分する点)
    # C(3, 0)からD(3, 3)へ向かって1:2の位置
    # y座標: 0 + (3-0) * (1 / (1+2)) = 1
    N = [3, 1]

    # プロットの準備
    fig, ax = plt.subplots(figsize=(6, 6))

    # 正方形の辺を描画 (A->B->C->D->A)
    square_x = [A[0], B[0], C[0], D[0], A[0]]
    square_y = [A[1], B[1], C[1], D[1], A[1]]
    ax.plot(square_x, square_y, color='black',\
            linewidth=2, label='Square ABCD')

    # 線分MNを描画
    ax.plot([M[0], N[0]], [M[1], N[1]], color='red',\
            linestyle='--', linewidth=2, label='Line MN')

    # 各点(A, B, C, D, M, N)をプロット
    points = {'A': A, 'B': B, 'C': C, 'D': D, 'M': M, 'N': N}
    for name, pos in points.items():
        ax.scatter(pos[0], pos[1], color='blue')
        ax.text(pos[0], pos[1], f' {name}', fontsize=12, \
                ha='right' if pos[0]==0 else 'left')

    # グラフの設定
    ax.set_aspect('equal') # 正方形を正しく表示するためにアスペクト比を固定
    ax.set_xlim(-1, 4)
    ax.set_ylim(-1, 4)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_title("Square ABCD with Line MN")
    ax.legend()

    plt.show()

# --- 実行例 ---
draw_square_with_line()