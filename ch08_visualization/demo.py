"""
第8章 演示代码：数据可视化
==========================
用生物信息学中常见的基因表达量数据，演示 Matplotlib 和 Seaborn 的核心绘图操作。

注意：本脚本使用 Agg 后端，无需 GUI 环境即可保存图片。
"""

# ============================================================
# 环境设置（必须在导入 pyplot 之前）
# ============================================================
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端，不需要显示器也能保存图片

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

# 设置中文字体（如果系统没有中文字体，标题会显示方框，但不影响保存）
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 图片保存路径：保存到当前脚本所在目录
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))


def save_figure(fig, filename):
    """保存图片到脚本所在目录，并打印保存路径。"""
    filepath = os.path.join(SAVE_DIR, filename)
    fig.savefig(filepath, dpi=150, bbox_inches='tight')
    print(f"  -> 图片已保存: {filepath}")
    plt.close(fig)  # 关闭图形，释放内存


# ============================================================
# 演示1：折线图 -- 基因表达量随时间变化
# ============================================================
# 场景：观察基因 TP53 在药物处理后 5 个时间点的表达变化

print("=" * 60)
print("演示1：折线图 -- 基因表达量随时间变化")
print("=" * 60)

# 模拟数据：5个时间点（小时），TP53 的表达量（FPKM）
time_points = np.array([0, 6, 12, 24, 48])
tp53_expr = np.array([5.2, 8.1, 12.5, 15.3, 14.8])    # 处理组：先上升后平台
tp53_ctrl = np.array([5.0, 5.3, 4.8, 5.1, 5.2])        # 对照组：基本不变

# 创建画布和坐标轴
fig, ax = plt.subplots(figsize=(8, 5))

# 绘制两条折线
ax.plot(time_points, tp53_expr, marker='o', color='#e74c3c',
        linewidth=2, label='Treatment')
ax.plot(time_points, tp53_ctrl, marker='s', color='#3498db',
        linewidth=2, linestyle='--', label='Control')

# 美化图表
ax.set_title("TP53 Expression Over Time", fontsize=14)
ax.set_xlabel("Time (hours)", fontsize=12)
ax.set_ylabel("Expression (FPKM)", fontsize=12)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

save_figure(fig, "demo1_line_plot.png")


# ============================================================
# 演示2：散点图 -- 两个基因表达量的相关性
# ============================================================
# 场景：TP53 和 MDM2 是已知的调控关系，观察它们的表达是否相关

print("\n" + "=" * 60)
print("演示2：散点图 -- 两个基因表达量的相关性")
print("=" * 60)

# 模拟数据：30个样本中两个基因的表达量
np.random.seed(42)  # 固定随机种子，确保可复现
tp53_values = np.random.normal(loc=10, scale=3, size=30)        # TP53 表达量
mdm2_values = tp53_values * 0.8 + np.random.normal(0, 1.5, 30) # MDM2 与 TP53 正相关

# 计算相关系数
correlation = np.corrcoef(tp53_values, mdm2_values)[0, 1]
print(f"  TP53 与 MDM2 的相关系数: {correlation:.3f}")

# 绘制散点图
fig, ax = plt.subplots(figsize=(7, 6))

ax.scatter(tp53_values, mdm2_values, color='#2ecc71', alpha=0.7,
           edgecolors='white', s=60)

# 添加趋势线（一次多项式拟合）
z = np.polyfit(tp53_values, mdm2_values, 1)  # 线性拟合
p = np.poly1d(z)
x_line = np.linspace(tp53_values.min(), tp53_values.max(), 100)
ax.plot(x_line, p(x_line), color='#e74c3c', linewidth=2,
        linestyle='--', label=f'r = {correlation:.3f}')

# 美化
ax.set_title("TP53 vs MDM2 Expression Correlation", fontsize=14)
ax.set_xlabel("TP53 Expression (FPKM)", fontsize=12)
ax.set_ylabel("MDM2 Expression (FPKM)", fontsize=12)
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)

save_figure(fig, "demo2_scatter_plot.png")


# ============================================================
# 演示3：柱状图 -- 不同样本中 TP53 表达量对比
# ============================================================
# 场景：比较 6 个患者样本中 TP53 基因的表达量

print("\n" + "=" * 60)
print("演示3：柱状图 -- 不同样本中 TP53 表达量对比")
print("=" * 60)

# 模拟数据
samples = ["Patient_1", "Patient_2", "Patient_3",
           "Patient_4", "Patient_5", "Patient_6"]
tp53_expression = np.array([12.5, 3.8, 15.2, 8.7, 2.1, 11.3])

# 根据表达量高低设置不同颜色
colors = ['#e74c3c' if val > 10 else '#3498db' for val in tp53_expression]

# 绘制柱状图
fig, ax = plt.subplots(figsize=(9, 5))

bars = ax.bar(samples, tp53_expression, color=colors, edgecolor='white',
              width=0.6)

# 在每个柱子顶部标注数值
for bar, val in zip(bars, tp53_expression):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', fontsize=10)

# 添加阈值线（如：正常表达阈值）
ax.axhline(y=10, color='gray', linestyle='--', alpha=0.7, label='Threshold = 10')

# 美化
ax.set_title("TP53 Expression Across Patients", fontsize=14)
ax.set_xlabel("Sample", fontsize=12)
ax.set_ylabel("Expression (FPKM)", fontsize=12)
ax.legend(fontsize=10)

save_figure(fig, "demo3_bar_plot.png")


# ============================================================
# 演示4：热图 -- 基因表达矩阵可视化
# ============================================================
# 场景：5个基因 × 4个样本的表达矩阵热图（生信标配图！）

print("\n" + "=" * 60)
print("演示4：热图 -- 基因表达矩阵可视化")
print("=" * 60)

# 模拟数据：5个基因在4个样本中的表达量
gene_names = ["TP53", "BRCA1", "EGFR", "MYC", "GAPDH"]
sample_names = ["Tumor_1", "Tumor_2", "Normal_1", "Normal_2"]

# 用 numpy 生成模拟表达数据
np.random.seed(123)
expr_data = np.array([
    [12.5,  8.3,  5.2,  4.8],   # TP53:  肿瘤中高表达
    [ 3.2,  2.8, 10.5, 11.2],   # BRCA1: 正常中高表达
    [18.7, 20.1,  6.3,  5.9],   # EGFR:  肿瘤中高表达
    [15.3, 17.8,  3.1,  2.5],   # MYC:   肿瘤中高表达
    [50.2, 49.8, 51.3, 50.5],   # GAPDH: 表达稳定（管家基因）
])

# 创建 DataFrame（seaborn 的 heatmap 可以直接用 DataFrame 的行名和列名）
df_expr = pd.DataFrame(expr_data, index=gene_names, columns=sample_names)
print("表达矩阵：")
print(df_expr)

# 绘制热图
fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(
    df_expr,
    annot=True,        # 在每个格子中显示数值
    fmt=".1f",         # 数值格式：保留1位小数
    cmap="RdBu_r",     # 颜色方案：红蓝渐变（红=高表达，蓝=低表达）
    linewidths=0.5,    # 格子之间的线宽
    ax=ax,
)

ax.set_title("Gene Expression Heatmap", fontsize=14)
ax.set_ylabel("Gene", fontsize=12)
ax.set_xlabel("Sample", fontsize=12)

save_figure(fig, "demo4_heatmap.png")


# ============================================================
# 演示5：子图组合 -- 多张图放在一起展示
# ============================================================
# 场景：一张图中同时展示折线图、散点图、柱状图和箱线图

print("\n" + "=" * 60)
print("演示5：子图组合 -- 四图合一")
print("=" * 60)

# 创建 2×2 的子图布局
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# --- 子图1 (左上)：折线图 ---
axes[0, 0].plot(time_points, tp53_expr, marker='o', color='#e74c3c', label='Treatment')
axes[0, 0].plot(time_points, tp53_ctrl, marker='s', color='#3498db',
                linestyle='--', label='Control')
axes[0, 0].set_title("A. Expression Over Time", fontsize=12)
axes[0, 0].set_xlabel("Time (h)")
axes[0, 0].set_ylabel("FPKM")
axes[0, 0].legend(fontsize=9)
axes[0, 0].grid(True, alpha=0.3)

# --- 子图2 (右上)：散点图 ---
axes[0, 1].scatter(tp53_values, mdm2_values, color='#2ecc71', alpha=0.7,
                   edgecolors='white', s=50)
axes[0, 1].set_title("B. TP53 vs MDM2 Correlation", fontsize=12)
axes[0, 1].set_xlabel("TP53 (FPKM)")
axes[0, 1].set_ylabel("MDM2 (FPKM)")
axes[0, 1].grid(True, alpha=0.3)

# --- 子图3 (左下)：柱状图 ---
bar_colors = ['#e74c3c' if v > 10 else '#3498db' for v in tp53_expression]
axes[1, 0].bar(samples, tp53_expression, color=bar_colors, edgecolor='white')
axes[1, 0].set_title("C. TP53 Across Patients", fontsize=12)
axes[1, 0].set_ylabel("FPKM")
axes[1, 0].tick_params(axis='x', rotation=30)

# --- 子图4 (右下)：箱线图 ---
# 用前面热图的数据，展示肿瘤 vs 正常的分布差异
boxplot_data = pd.DataFrame({
    'Expression': np.concatenate([expr_data[:, :2].flatten(),
                                  expr_data[:, 2:].flatten()]),
    'Group': (['Tumor'] * 10 + ['Normal'] * 10),
    'Gene': (gene_names * 2 + gene_names * 2),
})
sns.boxplot(data=boxplot_data, x='Group', y='Expression', hue='Group',
            ax=axes[1, 1], legend=False,
            palette={'Tumor': '#e74c3c', 'Normal': '#3498db'})
axes[1, 1].set_title("D. Expression Distribution", fontsize=12)
axes[1, 1].set_ylabel("FPKM")

# 自动调整子图间距，避免标签重叠
fig.tight_layout()

save_figure(fig, "demo5_subplots.png")


# ============================================================
# 小结
# ============================================================
print("\n" + "=" * 60)
print("本章演示总结")
print("=" * 60)
print(f"""
1. 折线图 plt.plot()    -> demo1_line_plot.png
2. 散点图 plt.scatter() -> demo2_scatter_plot.png
3. 柱状图 plt.bar()     -> demo3_bar_plot.png
4. 热图   sns.heatmap() -> demo4_heatmap.png
5. 子图   plt.subplots  -> demo5_subplots.png

所有图片保存在: {SAVE_DIR}
""")
