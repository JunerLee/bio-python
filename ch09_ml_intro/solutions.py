"""
第9章 练习题：机器学习入门
=========================
前置知识：已学完本章讲义和 demo.py 代码演示。
本文件已补全参考答案，可直接运行查看结果。
"""

import matplotlib
matplotlib.use('Agg')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ============================================================
# 数据准备（两道练习共用）
# ============================================================
# 加载数据并划分训练集/测试集，与 demo.py 中一致
iris = load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


# ============================================================
# 练习1：随机森林分类，并与 KNN 和决策树对比准确率
# ============================================================
# 随机森林 = 多棵决策树投票，通常比单棵决策树更稳定、更准确。
#
# 任务：
#   1. 创建随机森林模型（RandomForestClassifier）
#   2. 用训练数据拟合模型
#   3. 用测试数据预测
#   4. 计算准确率
#   5. 与 KNN 和决策树的准确率进行对比
#
# 提示：
#   - RandomForestClassifier 的用法与 DecisionTreeClassifier 完全一致
#   - 参数 n_estimators 控制森林中树的数量，默认100棵
#   - 记得设置 random_state=42 保证结果可复现
# ============================================================

print("=" * 60)
print("练习1：随机森林 vs KNN vs 决策树")
print("=" * 60)

# --- KNN（已完成，供参考）---
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train_scaled, y_train)
y_pred_knn = knn.predict(X_test_scaled)
acc_knn = accuracy_score(y_test, y_pred_knn)

# --- 决策树（已完成，供参考）---
dt = DecisionTreeClassifier(random_state=42)
dt.fit(X_train_scaled, y_train)
y_pred_dt = dt.predict(X_test_scaled)
acc_dt = accuracy_score(y_test, y_pred_dt)

# --- 随机森林（参考答案）---

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
acc_rf = accuracy_score(y_test, y_pred_rf)

# --- 对比结果 ---
print(f"KNN (k=5)   准确率: {acc_knn:.4f}")
print(f"决策树      准确率: {acc_dt:.4f}")
print(f"随机森林    准确率: {acc_rf:.4f}")
print()
print("思考：随机森林的准确率是否高于单棵决策树？为什么？")


# ============================================================
# 练习2：调整 KNN 的 k 值，找出最佳 k
# ============================================================
# KNN 中 k 是一个"超参数"——需要我们人为设定的参数。
# k 太小（如1），模型容易受噪声影响（过拟合）；
# k 太大（如149），模型太粗糙，失去区分能力（欠拟合）。
#
# 任务：
#   1. 尝试 k = 1, 3, 5, 7, 9
#   2. 分别计算每个 k 值对应的准确率
#   3. 找出最佳 k 值
#   4.（可选）画出 k 值与准确率的折线图
#
# 提示：
#   - 用 for 循环遍历不同的 k 值
#   - KNeighborsClassifier(n_neighbors=k)
#   - 把每个 k 对应的准确率存入列表
# ============================================================

print("\n" + "=" * 60)
print("练习2：调整 KNN 的 k 值")
print("=" * 60)

k_values = [1, 3, 5, 7, 9]
accuracies = []

for k in k_values:
    knn_k = KNeighborsClassifier(n_neighbors=k)
    knn_k.fit(X_train_scaled, y_train)
    y_pred_k = knn_k.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred_k)
    accuracies.append(acc)

    print(f"k = {k}  准确率: {acc:.4f}")

best_idx = int(np.argmax(accuracies))

if best_idx is not None:
    print(f"\n最佳 k 值: {k_values[best_idx]}，准确率: {accuracies[best_idx]:.4f}")
else:
    print("\n最佳 k 值暂未计算，请检查实现。")

plt.figure(figsize=(8, 5))
plt.plot(k_values, accuracies, marker='o', linewidth=2, markersize=8)
plt.xlabel('k value')
plt.ylabel('Accuracy')
plt.title('KNN Accuracy vs. k Value')
plt.xticks(k_values)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plot_path = Path(__file__).with_name("knn_k_values.png")
plt.savefig(plot_path, dpi=150)
plt.close()
print(f"折线图已保存: {plot_path}")

print("\n" + "=" * 60)
print("思考题：")
print("1. k=1 时准确率如何？为什么 k=1 容易过拟合？")
print("2. k 值越大一定越好吗？为什么？")
print("3. 在实际研究中，我们通常如何选择最佳超参数？")
print("   （提示：搜索「交叉验证 cross-validation」）")
print("=" * 60)
