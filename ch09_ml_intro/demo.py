"""
第9章 代码演示：鸢尾花（Iris）分类完整案例
=============================================
目标：用机器学习模型根据花的测量数据自动识别鸢尾花品种。

鸢尾花数据集包含 150 个样本，3 个品种（setosa、versicolor、virginica），
每个样本有 4 个特征：花萼长度、花萼宽度、花瓣长度、花瓣宽度。

这是机器学习领域的经典入门数据集，就像生物学中的大肠杆菌一样经典。
"""

# ============================================================
# 环境准备
# ============================================================
# 使用 Agg 后端，这样即使没有图形界面也能保存图片
import matplotlib
matplotlib.use('Agg')

from pathlib import Path
import numpy as np
import pandas as pd

OUTPUT_DIR = Path(__file__).parent
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay

# 设置中文字体（如果系统支持），否则使用默认字体
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ============================================================
# 第1步：加载数据
# ============================================================
# sklearn 内置了鸢尾花数据集，无需下载文件
iris = load_iris()

# 将数据转为 DataFrame，方便查看和操作
# iris.data 是特征矩阵（数值），iris.target 是类别标签（0/1/2）
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['species'] = iris.target  # 添加品种标签列

print("=" * 60)
print("第1步：加载数据")
print("=" * 60)
print(f"数据集形状: {df.shape}")
print(f"即 {df.shape[0]} 个样本，{df.shape[1] - 1} 个特征 + 1 个标签列")
print(f"\n品种编号对应关系: {dict(enumerate(iris.target_names))}")


# ============================================================
# 第2步：数据探索
# ============================================================
print("\n" + "=" * 60)
print("第2步：数据探索")
print("=" * 60)

# 查看基本统计信息：均值、标准差、最大最小值等
print("\n基本统计信息：")
print(df.describe().round(2))

# 查看各品种的样本数量 —— 确认数据是否均衡
# 不均衡的数据会让模型偏向多数类，就像一个班级90%是男生，
# 猜"男生"就能达到90%准确率，但这并不代表模型真正学会了分类
print("\n各品种样本数：")
print(df['species'].value_counts().sort_index())


# ============================================================
# 第3步：数据可视化
# ============================================================
# 用散点图直观感受不同品种在特征空间中的分布
# 选择花瓣长度和花瓣宽度这两个特征，因为它们对品种区分度最高
print("\n" + "=" * 60)
print("第3步：数据可视化（保存散点图）")
print("=" * 60)

fig, ax = plt.subplots(figsize=(8, 6))

colors = ['#e74c3c', '#2ecc71', '#3498db']
for i, species_name in enumerate(iris.target_names):
    mask = df['species'] == i
    ax.scatter(
        df.loc[mask, 'petal length (cm)'],
        df.loc[mask, 'petal width (cm)'],
        c=colors[i],
        label=species_name,
        alpha=0.7,
        edgecolors='white',
        s=80
    )

ax.set_xlabel('Petal Length (cm)')
ax.set_ylabel('Petal Width (cm)')
ax.set_title('Iris Dataset - Petal Features')
ax.legend(title='Species')
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'iris_scatter.png', dpi=150)
plt.close()
print("散点图已保存: iris_scatter.png")
print("观察：setosa 与其他两个品种明显分开，versicolor 和 virginica 有部分重叠")


# ============================================================
# 第4步：划分训练集和测试集
# ============================================================
# 就像教科书和考试的关系——训练集用来学习，测试集用来检验
print("\n" + "=" * 60)
print("第4步：划分训练集和测试集（80% 训练 / 20% 测试）")
print("=" * 60)

X = iris.data   # 特征矩阵：150 x 4
y = iris.target  # 标签向量：150 个值（0, 1, 2）

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,      # 20% 作为测试集
    random_state=42,     # 固定随机种子，保证每次运行结果一致
    stratify=y           # 分层抽样，保证训练集和测试集中各品种比例一致
)

print(f"训练集大小: {X_train.shape[0]} 个样本")
print(f"测试集大小: {X_test.shape[0]} 个样本")


# ============================================================
# 第5步：数据标准化
# ============================================================
# 为什么要标准化？
# 花萼长度范围约 4~8 cm，花瓣宽度范围约 0.1~2.5 cm
# 如果不标准化，数值大的特征会对KNN的距离计算产生更大影响
# 标准化后所有特征都在相同尺度上，每个特征被公平对待
print("\n" + "=" * 60)
print("第5步：数据标准化")
print("=" * 60)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)  # 在训练集上计算均值和标准差，然后转换
X_test_scaled = scaler.transform(X_test)          # 用训练集的参数转换测试集（不能重新fit！）

print("标准化前（训练集前3个样本）：")
print(X_train[:3].round(2))
print("\n标准化后（训练集前3个样本）：")
print(X_train_scaled[:3].round(2))
print("\n可以看到，标准化后数据以0为中心，量纲统一")


# ============================================================
# 第6步：KNN 模型训练与预测
# ============================================================
# KNN 的思路："告诉我你的邻居是谁，我就知道你是谁"
# 默认 k=5，即找最近的5个邻居来投票决定类别
print("\n" + "=" * 60)
print("第6步：KNN 模型训练与预测")
print("=" * 60)

knn = KNeighborsClassifier(n_neighbors=5)  # 创建KNN模型，k=5
knn.fit(X_train_scaled, y_train)           # 用训练数据"教"模型
y_pred_knn = knn.predict(X_test_scaled)    # 用模型预测测试数据的类别

knn_accuracy = accuracy_score(y_test, y_pred_knn)
print(f"KNN 准确率: {knn_accuracy:.4f}")
print(f"即 {int(knn_accuracy * len(y_test))}/{len(y_test)} 个样本预测正确")


# ============================================================
# 第7步：决策树模型训练与预测
# ============================================================
# 决策树的思路：像分类检索表一样，逐步提问来缩小范围
# 注意：决策树不需要标准化（它基于特征的大小关系，不受尺度影响）
# 但为了公平对比，我们仍然使用标准化后的数据
print("\n" + "=" * 60)
print("第7步：决策树模型训练与预测")
print("=" * 60)

dt = DecisionTreeClassifier(random_state=42)  # 创建决策树模型
dt.fit(X_train_scaled, y_train)               # 训练
y_pred_dt = dt.predict(X_test_scaled)         # 预测

dt_accuracy = accuracy_score(y_test, y_pred_dt)
print(f"决策树准确率: {dt_accuracy:.4f}")
print(f"即 {int(dt_accuracy * len(y_test))}/{len(y_test)} 个样本预测正确")


# ============================================================
# 第8步：模型对比
# ============================================================
print("\n" + "=" * 60)
print("第8步：模型对比")
print("=" * 60)

results = pd.DataFrame({
    '模型': ['KNN (k=5)', '决策树'],
    '准确率': [knn_accuracy, dt_accuracy]
})
print(results.to_string(index=False))

if knn_accuracy > dt_accuracy:
    print("\n结论：在本次实验中，KNN 表现更好")
elif knn_accuracy < dt_accuracy:
    print("\n结论：在本次实验中，决策树表现更好")
else:
    print("\n结论：在本次实验中，两个模型表现相当")


# ============================================================
# 第9步：混淆矩阵可视化
# ============================================================
# 混淆矩阵告诉我们：每个品种有多少被正确分类，多少被误判为其他品种
# 对角线上的数值越大越好（代表正确分类）
print("\n" + "=" * 60)
print("第9步：混淆矩阵可视化（保存图片）")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# KNN 的混淆矩阵
cm_knn = confusion_matrix(y_test, y_pred_knn)
disp_knn = ConfusionMatrixDisplay(cm_knn, display_labels=iris.target_names)
disp_knn.plot(ax=axes[0], cmap='Blues', colorbar=False)
axes[0].set_title('KNN Confusion Matrix')

# 决策树的混淆矩阵
cm_dt = confusion_matrix(y_test, y_pred_dt)
disp_dt = ConfusionMatrixDisplay(cm_dt, display_labels=iris.target_names)
disp_dt.plot(ax=axes[1], cmap='Greens', colorbar=False)
axes[1].set_title('Decision Tree Confusion Matrix')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / 'confusion_matrix.png', dpi=150)
plt.close()
print("混淆矩阵已保存: confusion_matrix.png")

print("\nKNN 混淆矩阵（数值）：")
print(cm_knn)
print("\n决策树混淆矩阵（数值）：")
print(cm_dt)


# ============================================================
# 第10步：分类报告
# ============================================================
# 分类报告比准确率更详细，展示每个类别的精确率、召回率和 F1 分数
print("\n" + "=" * 60)
print("第10步：分类报告")
print("=" * 60)

print("\n--- KNN 分类报告 ---")
print(classification_report(y_test, y_pred_knn, target_names=iris.target_names))

print("--- 决策树分类报告 ---")
print(classification_report(y_test, y_pred_dt, target_names=iris.target_names))

print("=" * 60)
print("演示完毕！你已经完成了一个完整的机器学习分类流程。")
print("=" * 60)
