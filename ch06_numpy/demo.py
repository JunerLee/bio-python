"""
第6章 演示代码：NumPy 快速入门
================================
用生物信息学中常见的基因表达量数据，演示 NumPy 的核心操作。
"""

import numpy as np

# ============================================================
# 演示1：一维数组 -- 单个基因的表达量分析
# ============================================================
# 场景：基因 TP53 在 5 个肿瘤样本中的表达量（单位：FPKM）

print("=" * 60)
print("演示1：单个基因的表达量分析")
print("=" * 60)

tp53_expr = np.array([12.5, 8.3, 15.7, 6.1, 11.2])

print(f"TP53 表达量: {tp53_expr}")
print(f"数组形状: {tp53_expr.shape}")   # (5,) -- 5个元素的一维数组
print(f"数据类型: {tp53_expr.dtype}")   # float64

# 基本统计量 -- 只需调用方法，无需写循环
print(f"均值:   {tp53_expr.mean():.2f}")
print(f"标准差: {tp53_expr.std():.2f}")
print(f"最小值: {tp53_expr.min():.2f}")
print(f"最大值: {tp53_expr.max():.2f}")
print(f"中位数: {np.median(tp53_expr):.2f}")

# ============================================================
# 演示2：二维数组 -- 基因×样本表达矩阵
# ============================================================
# 场景：3个基因在4个样本中的表达矩阵
#       行 = 基因，列 = 样本

print("\n" + "=" * 60)
print("演示2：基因×样本表达矩阵")
print("=" * 60)

gene_names = ["TP53", "BRCA1", "EGFR"]
sample_names = ["样本A", "样本B", "样本C", "样本D"]

# 创建 3行4列 的表达矩阵
expr_matrix = np.array([
    [12.5,  8.3, 15.7,  6.1],  # TP53
    [ 3.2,  1.5,  4.8,  2.9],  # BRCA1
    [25.1, 22.7, 18.3, 20.5],  # EGFR
])

print(f"表达矩阵:\n{expr_matrix}")
print(f"形状: {expr_matrix.shape}")  # (3, 4) -- 3个基因 x 4个样本

# axis=1：沿列方向计算 -> 每个基因在所有样本中的均值
gene_means = expr_matrix.mean(axis=1)
print("\n每个基因的平均表达量 (axis=1):")
for name, mean_val in zip(gene_names, gene_means):
    print(f"  {name}: {mean_val:.2f}")

# axis=0：沿行方向计算 -> 每个样本中所有基因的均值
sample_means = expr_matrix.mean(axis=0)
print("\n每个样本的平均表达量 (axis=0):")
for name, mean_val in zip(sample_names, sample_means):
    print(f"  {name}: {mean_val:.2f}")

# ============================================================
# 演示3：布尔索引 -- 筛选高表达基因
# ============================================================
# 场景：找出在样本A中表达量 > 10 的基因

print("\n" + "=" * 60)
print("演示3：布尔索引 -- 筛选高表达基因")
print("=" * 60)

# 取出样本A（第0列）的所有基因表达量
sample_a = expr_matrix[:, 0]
print(f"样本A 各基因表达量: {sample_a}")

# 设定阈值，生成布尔掩码
threshold = 10.0
mask = sample_a > threshold
print(f"阈值 > {threshold} 的掩码: {mask}")  # [True, False, True]

# 用布尔掩码筛选
high_genes = np.array(gene_names)[mask]
high_values = sample_a[mask]
print(f"高表达基因: {high_genes}")
print(f"对应表达量: {high_values}")

# 也可以对整个矩阵做布尔筛选：找出矩阵中所有 > 20 的值
print(f"\n矩阵中所有 > 20 的表达值: {expr_matrix[expr_matrix > 20]}")

# ============================================================
# 演示4：log2 转换 -- 真实生信分析的标准步骤
# ============================================================
# 场景：RNA-seq 数据分析中，常对表达量做 log2 转换
# 原因：原始表达量的分布通常是右偏的，log 转换后更接近正态分布
# 注意：需要加一个小数（伪计数）避免 log2(0) = -inf

print("\n" + "=" * 60)
print("演示4：log2 转换")
print("=" * 60)

print(f"原始表达矩阵:\n{expr_matrix}")

# 加伪计数 1，再取 log2（生信标准做法）
log2_matrix = np.log2(expr_matrix + 1)

print(f"\nlog2(x+1) 转换后:\n{np.round(log2_matrix, 2)}")

# 验证：log2(12.5 + 1) = log2(13.5) ≈ 3.75
print(f"\n验证：log2(12.5 + 1) = {np.log2(12.5 + 1):.2f}")

# 转换前后的范围对比
print(f"\n转换前 -- 最小值: {expr_matrix.min():.1f}, 最大值: {expr_matrix.max():.1f}")
print(f"转换后 -- 最小值: {log2_matrix.min():.2f}, 最大值: {log2_matrix.max():.2f}")
print("可以看到 log2 转换后，数值范围被压缩，极端值的影响减小。")

# ============================================================
# 小结
# ============================================================
print("\n" + "=" * 60)
print("本章核心操作总结")
print("=" * 60)
print("""
1. np.array()     -- 创建数组
2. .mean/.std     -- 统计计算（配合 axis 参数）
3. array[条件]    -- 布尔索引筛选
4. np.log2()      -- 元素级数学函数
5. axis=0 跨行（跨基因），axis=1 跨列（跨样本）
""")
