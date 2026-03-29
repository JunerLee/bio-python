"""
第8章 练习题：数据可视化实战
============================
通过绘制生信经典图形，练习 Matplotlib 和 Seaborn 的核心操作。

注意：本脚本使用 Agg 后端，无需 GUI 环境即可保存图片。
"""

# ============================================================
# 环境设置（必须在导入 pyplot 之前）
# ============================================================
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

# 图片保存路径
SAVE_DIR = os.path.dirname(os.path.abspath(__file__))

# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


# ============================================================
# 练习1：分组柱状图 -- Cancer vs Normal 基因表达量对比
# ============================================================
"""
【背景】
在肿瘤研究中，我们经常需要比较同一个基因在肿瘤组（Cancer）和正常组（Normal）
中的平均表达量。分组柱状图（Grouped Bar Chart）是展示这种对比的经典方式：
每个基因对应两根柱子，一根代表 Cancer 组，一根代表 Normal 组。

【任务】
用下面提供的模拟数据，绘制一张分组柱状图：
- X 轴：5个基因名称
- Y 轴：平均表达量（TPM）
- 每个基因有两根柱子：Cancer（红色）和 Normal（蓝色）
- 添加标题、轴标签、图例
- 保存为 "exercise1_grouped_bar.png"

【模拟数据】
"""

# --- 模拟数据 ---
gene_names = ["TP53", "BRCA1", "EGFR", "MYC", "GAPDH"]

# 5个基因在 Cancer 组的平均表达量
cancer_mean = np.array([15.3, 4.2, 22.8, 18.5, 50.1])

# 5个基因在 Normal 组的平均表达量
normal_mean = np.array([6.8, 11.5, 7.2, 3.9, 49.8])

"""
【提示 - 分步完成】

步骤1：理解分组柱状图的原理
  - 每个基因位置有两根柱子，需要把它们并排放置
  - 关键技巧：用 np.arange() 生成基因的位置坐标，然后通过偏移来放置两组柱子

步骤2：计算柱子位置
  x = np.arange(len(gene_names))  # 基因位置：[0, 1, 2, 3, 4]
  width = 0.35                     # 每根柱子的宽度
  # Cancer 组的柱子位置：x - width/2（左移半个柱宽）
  # Normal 组的柱子位置：x + width/2（右移半个柱宽）

步骤3：绘制柱状图
  fig, ax = plt.subplots(figsize=(10, 6))
  # ax.bar(Cancer位置, cancer_mean, width, label=..., color=...)
  # ax.bar(Normal位置, normal_mean, width, label=..., color=...)

步骤4：美化
  # ax.set_xticks(x)                     -- 刻度位置
  # ax.set_xticklabels(gene_names)       -- 刻度标签
  # ax.set_title(...)、ax.set_ylabel(...)
  # ax.legend()

步骤5：保存
  plt.savefig(os.path.join(SAVE_DIR, "exercise1_grouped_bar.png"),
              dpi=150, bbox_inches='tight')
  plt.close(fig)

【思考题】
- 从图中可以看出哪些基因在肿瘤中高表达？哪些在正常组织中高表达？
- GAPDH 的表达量在两组中有何特点？这与它作为管家基因的角色是否一致？
"""

# ----- 参考答案 -----
x = np.arange(len(gene_names))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width / 2, cancer_mean, width, label="Cancer", color="#e74c3c")
ax.bar(x + width / 2, normal_mean, width, label="Normal", color="#3498db")

ax.set_xticks(x)
ax.set_xticklabels(gene_names)
ax.set_title("Cancer vs Normal Gene Expression", fontsize=14)
ax.set_xlabel("Gene", fontsize=12)
ax.set_ylabel("Mean Expression (TPM)", fontsize=12)
ax.legend()
ax.grid(axis="y", alpha=0.3)

exercise1_path = os.path.join(SAVE_DIR, "exercise1_grouped_bar.png")
plt.savefig(exercise1_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"练习1图片已保存: {exercise1_path}")




# ============================================================
# 练习2：火山图（Volcano Plot） -- 差异表达分析经典图形
# ============================================================
"""
【背景】
火山图是生物信息学中最经典的图形之一，用于展示差异表达分析的结果。
它以"火山喷发"的形状得名：
- X 轴：log2FoldChange（表达量变化的对数值）
  - 正值 = 在实验组中上调
  - 负值 = 在实验组中下调
  - 值越大，表达变化越剧烈
- Y 轴：-log10(pvalue)（统计显著性的对数值）
  - 值越大，统计上越显著
  - pvalue 越小 -> -log10 值越大 -> 图上越靠上

通常我们会设定两个阈值来筛选"差异显著基因"：
  1. |log2FoldChange| > 1  （表达量变化超过2倍）
  2. pvalue < 0.05          （统计上显著）

满足两个条件的基因会被标记为红色（上调）或蓝色（下调）。

【任务】
用下面提供的模拟数据，绘制一张火山图：
1. 所有基因画成灰色散点
2. 显著上调基因（log2FC > 1 且 pvalue < 0.05）标记为红色
3. 显著下调基因（log2FC < -1 且 pvalue < 0.05）标记为蓝色
4. 添加阈值线（水平线和垂直线）
5. 添加标题、轴标签
6. 保存为 "exercise2_volcano_plot.png"

【模拟数据】
"""

# --- 模拟数据：200个基因的差异表达结果 ---
np.random.seed(2024)
n_genes = 200

# 大部分基因变化不大（集中在中间），少部分变化显著（分布在两侧）
log2fc = np.random.normal(0, 1.2, n_genes)

# p 值：与 |log2fc| 正相关（变化越大的基因，p值倾向于越小）
pvalue = 10 ** (-np.abs(log2fc) * np.random.uniform(0.5, 2.5, n_genes))
pvalue = np.clip(pvalue, 1e-10, 1.0)  # 限制范围

# 计算 Y 轴值：-log10(pvalue)
neg_log10_p = -np.log10(pvalue)

# 整理为 DataFrame（便于查看和操作）
df_volcano = pd.DataFrame({
    'log2FoldChange': log2fc,
    'pvalue': pvalue,
    'neg_log10_pvalue': neg_log10_p,
})

print("火山图数据预览（前10行）：")
print(df_volcano.head(10))
print(f"\n总基因数: {n_genes}")

"""
【提示 - 分步完成】

步骤1：定义阈值
  fc_threshold = 1      # |log2FoldChange| > 1
  p_threshold = 0.05    # pvalue < 0.05

步骤2：用布尔索引给基因分类
  # 上调基因：log2FC > 1 且 pvalue < 0.05
  up = (df_volcano['log2FoldChange'] > fc_threshold) & (df_volcano['pvalue'] < p_threshold)
  # 下调基因：log2FC < -1 且 pvalue < 0.05
  down = (df_volcano['log2FoldChange'] < -fc_threshold) & (df_volcano['pvalue'] < p_threshold)
  # 不显著的基因
  not_sig = ~(up | down)

步骤3：绘制散点图（分三批画，颜色不同）
  fig, ax = plt.subplots(figsize=(8, 6))
  # ax.scatter(不显著基因的x, 不显著基因的y, color='gray', alpha=0.5, s=20)
  # ax.scatter(上调基因的x, 上调基因的y, color='red', alpha=0.7, s=30)
  # ax.scatter(下调基因的x, 下调基因的y, color='blue', alpha=0.7, s=30)

步骤4：添加阈值线
  # ax.axhline(y=-np.log10(0.05), ...)   -- 水平线：p=0.05 的位置
  # ax.axvline(x=1, ...)                  -- 垂直线：log2FC=1
  # ax.axvline(x=-1, ...)                 -- 垂直线：log2FC=-1

步骤5：美化并保存
  # 标题："Volcano Plot"
  # X轴："log2(Fold Change)"
  # Y轴："-log10(p-value)"
  # 图例标注三类基因的数量，如 "Up (N=xx)"

【思考题】
- 火山图为什么叫"火山图"？它的形状像什么？
- 图中左上角和右上角的点代表什么生物学意义？
- 为什么要同时考虑 FoldChange 和 pvalue 两个条件？
"""

# ----- 参考答案 -----
fc_threshold = 1
p_threshold = 0.05

up = (df_volcano['log2FoldChange'] > fc_threshold) & (df_volcano['pvalue'] < p_threshold)
down = (df_volcano['log2FoldChange'] < -fc_threshold) & (df_volcano['pvalue'] < p_threshold)
not_sig = ~(up | down)

fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(
    df_volcano.loc[not_sig, 'log2FoldChange'],
    df_volcano.loc[not_sig, 'neg_log10_pvalue'],
    color='gray', alpha=0.5, s=20, label=f'Not significant (N={not_sig.sum()})'
)
ax.scatter(
    df_volcano.loc[up, 'log2FoldChange'],
    df_volcano.loc[up, 'neg_log10_pvalue'],
    color='red', alpha=0.7, s=30, label=f'Up (N={up.sum()})'
)
ax.scatter(
    df_volcano.loc[down, 'log2FoldChange'],
    df_volcano.loc[down, 'neg_log10_pvalue'],
    color='blue', alpha=0.7, s=30, label=f'Down (N={down.sum()})'
)

ax.axhline(y=-np.log10(p_threshold), color='black', linestyle='--', linewidth=1)
ax.axvline(x=fc_threshold, color='black', linestyle='--', linewidth=1)
ax.axvline(x=-fc_threshold, color='black', linestyle='--', linewidth=1)

ax.set_title("Volcano Plot", fontsize=14)
ax.set_xlabel("log2(Fold Change)", fontsize=12)
ax.set_ylabel("-log10(p-value)", fontsize=12)
ax.legend()
ax.grid(alpha=0.2)

exercise2_path = os.path.join(SAVE_DIR, "exercise2_volcano_plot.png")
plt.savefig(exercise2_path, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"练习2图片已保存: {exercise2_path}")
