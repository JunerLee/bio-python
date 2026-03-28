"""
第10章 毕业挑战练习

练习1：神经网络 vs 随机森林
    - 使用 sklearn 的 MLPClassifier 构建神经网络
    - 与 RandomForestClassifier 在乳腺癌数据集上对比

练习2：PCA 降维可视化
    - 将 30 维特征降到 2 维
    - 绘制散点图观察良性/恶性样本在低维空间是否可分
"""

import matplotlib

matplotlib.use("Agg")

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

OUTPUT_DIR = Path(__file__).parent
RANDOM_STATE = 42


# ============================================================
# 练习1：神经网络 vs 随机森林
# ============================================================
# 目标：用 MLPClassifier（多层感知器）训练一个神经网络模型，
#       与随机森林在同一数据集上进行交叉验证对比，看谁更准确。
#
# MLPClassifier 简介：
#   - sklearn 中的神经网络分类器
#   - hidden_layer_sizes: 隐藏层结构，如 (64, 32) 表示两层，分别64和32个神经元
#   - max_iter: 最大迭代次数
#   - 神经网络对特征尺度敏感，必须先标准化！
#
# 提示：
#   1. 加载数据并标准化
#   2. 构建 MLPClassifier 和 RandomForestClassifier
#   3. 用 cross_val_score 做 5 折交叉验证
#   4. 打印并对比两者的准确率
# ============================================================


def exercise_1_nn_vs_rf() -> None:
    """练习1：比较神经网络和随机森林的分类性能。"""
    print("=" * 60)
    print("练习1：神经网络 vs 随机森林")
    print("=" * 60)

    # --- 数据准备 ---
    data = load_breast_cancer()
    X, y = data.data, data.target

    # 标准化（神经网络对此非常敏感）
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- TODO: 构建两个模型 ---
    # 提示：
    #   MLPClassifier(hidden_layer_sizes=?, max_iter=?, random_state=RANDOM_STATE)
    #   RandomForestClassifier(n_estimators=?, random_state=RANDOM_STATE)

    models = {
        "Random Forest": RandomForestClassifier(
            n_estimators=100,
            random_state=RANDOM_STATE,
        ),
        "Neural Network (MLP)": MLPClassifier(
            hidden_layer_sizes=(64, 32),  # 两层隐藏层：64 -> 32
            max_iter=1000,                # 充足的迭代次数
            random_state=RANDOM_STATE,
        ),
    }

    # --- TODO: 交叉验证对比 ---
    # 提示：对每个模型调用 cross_val_score(model, X_scaled, y, cv=5)
    # 注意：随机森林用原始数据 X 也可以，但为公平对比，这里统一用 X_scaled

    results = {}
    for name, model in models.items():
        scores = cross_val_score(model, X_scaled, y, cv=5, scoring="accuracy")
        results[name] = scores
        print(f"  {name:<25s}  准确率: {scores.mean():.4f} (+/- {scores.std():.4f})")

    # --- 结论 ---
    best = max(results, key=lambda k: results[k].mean())
    print(f"\n  结论: {best} 在本数据集上表现更好")
    print(f"  思考: 对于样本量较小（569例）的结构化数据，")
    print(f"        神经网络不一定比传统方法更优。")
    print(f"        深度学习的优势更多体现在大规模非结构化数据上。")


# ============================================================
# 练习2：PCA 降维可视化
# ============================================================
# 目标：用 PCA 将 30 维特征降到 2 维，绘制散点图，
#       观察良性和恶性样本在低维空间中是否可以分离。
#
# PCA 简介：
#   - 主成分分析（Principal Component Analysis）
#   - 找到数据方差最大的方向作为新的坐标轴
#   - n_components=2 表示降到 2 维
#   - 降维前需要标准化，因为 PCA 对尺度敏感
#
# 提示：
#   1. 加载数据并标准化
#   2. 用 PCA(n_components=2) 降维
#   3. 用不同颜色绘制两类样本的散点图
#   4. 标注坐标轴为 PC1 和 PC2，并注明方差解释比例
# ============================================================


def exercise_2_pca_visualization() -> None:
    """练习2：PCA 降维后可视化良性/恶性样本分布。"""
    print("\n" + "=" * 60)
    print("练习2：PCA 降维可视化")
    print("=" * 60)

    # --- 数据准备 ---
    data = load_breast_cancer()
    X, y = data.data, data.target
    target_names = data.target_names

    # 标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- TODO: PCA 降维 ---
    # 提示：
    #   pca = PCA(n_components=2)
    #   X_pca = pca.fit_transform(X_scaled)
    #   pca.explained_variance_ratio_ 可查看每个主成分解释的方差比例

    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # 打印方差解释比例
    var_ratio = pca.explained_variance_ratio_
    print(f"  PC1 方差解释比例: {var_ratio[0]:.4f} ({var_ratio[0]*100:.1f}%)")
    print(f"  PC2 方差解释比例: {var_ratio[1]:.4f} ({var_ratio[1]*100:.1f}%)")
    print(f"  前2个主成分累计: {var_ratio.sum():.4f} ({var_ratio.sum()*100:.1f}%)")

    # --- TODO: 绘制散点图 ---
    # 提示：
    #   - 用 plt.scatter 分别绘制 y==0（恶性）和 y==1（良性）
    #   - X_pca[:, 0] 是 PC1，X_pca[:, 1] 是 PC2
    #   - 用不同颜色区分两类

    plt.figure(figsize=(9, 7))

    colors = ["#e74c3c", "#2ecc71"]  # 红色=恶性，绿色=良性
    for label in [0, 1]:
        mask = y == label
        plt.scatter(
            X_pca[mask, 0],
            X_pca[mask, 1],
            c=colors[label],
            label=target_names[label],
            alpha=0.6,
            edgecolors="white",
            linewidth=0.5,
            s=50,
        )

    plt.xlabel(f"PC1 ({var_ratio[0]*100:.1f}% variance)", fontsize=12)
    plt.ylabel(f"PC2 ({var_ratio[1]*100:.1f}% variance)", fontsize=12)
    plt.title("PCA: Breast Cancer Samples in 2D Space", fontsize=14)
    plt.legend(fontsize=11, loc="best")
    plt.grid(alpha=0.3)
    plt.tight_layout()

    save_path = OUTPUT_DIR / "pca_visualization.png"
    plt.savefig(save_path, dpi=150)
    plt.close()

    print(f"\n  [已保存] PCA 可视化 -> {save_path}")
    print(f"  观察: 两类样本在 PC1 方向上有明显分离，")
    print(f"        说明线性方法（如逻辑回归）就能取得不错的分类效果。")


# ============================================================
# 主函数
# ============================================================
def main() -> None:
    """运行所有练习。"""
    print("*" * 60)
    print("  第10章 毕业挑战练习")
    print("*" * 60)

    exercise_1_nn_vs_rf()
    exercise_2_pca_visualization()

    print("\n" + "*" * 60)
    print("  所有练习完成！")
    print("*" * 60)


if __name__ == "__main__":
    main()
