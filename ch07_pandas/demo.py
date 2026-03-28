"""
第7章 代码演示：Pandas 基础操作
场景：分析一组模拟的基因表达数据（cancer vs normal）
"""

import pandas as pd
import numpy as np

# ============================================================
# 1. 创建模拟基因表达数据
# ============================================================
# 假设我们用 RNA-seq 检测了 5 个基因在 4 个样本中的表达量（TPM值）
# 其中 sample_1、sample_2 来自癌症组织，sample_3、sample_4 来自正常组织

print("=" * 60)
print("1. 创建基因表达 DataFrame")
print("=" * 60)

gene_expression = pd.DataFrame({
    '基因名':    ['TP53', 'BRCA1', 'MYC',  'EGFR', 'GAPDH'],
    'sample_1': [12.5,   3.2,     45.8,  28.3,   100.1],   # cancer
    'sample_2': [15.1,   2.9,     50.2,  32.7,   98.5],    # cancer
    'sample_3': [5.8,    8.1,     10.3,  6.2,    101.3],   # normal
    'sample_4': [6.2,    7.5,     12.1,  5.9,    99.7],    # normal
})

# 样本分组信息（单独记录每个样本属于哪个组）
sample_info = pd.DataFrame({
    '样本名': ['sample_1', 'sample_2', 'sample_3', 'sample_4'],
    '分组':   ['cancer',   'cancer',   'normal',   'normal'],
})

print(gene_expression)
print()
print("样本分组信息：")
print(sample_info)


# ============================================================
# 2. 基本探索：快速了解数据
# ============================================================
print("\n" + "=" * 60)
print("2. 基本探索")
print("=" * 60)

# head() — 查看前几行，确认数据读取正确
print("\n--- df.head(3)：查看前3行 ---")
print(gene_expression.head(3))

# shape — 数据的"尺寸"：几行几列
print(f"\n--- df.shape：{gene_expression.shape} （5个基因 × 5列）---")

# columns — 列名列表
print(f"\n--- df.columns：{list(gene_expression.columns)} ---")

# dtypes — 每列数据类型
print("\n--- df.dtypes ---")
print(gene_expression.dtypes)

# describe() — 数值列的统计摘要（均值、标准差、最大最小值等）
print("\n--- df.describe()：数值摘要 ---")
print(gene_expression.describe())


# ============================================================
# 3. 条件过滤：筛选感兴趣的数据
# ============================================================
print("\n" + "=" * 60)
print("3. 条件过滤")
print("=" * 60)

# 场景 A：筛选 cancer 组的样本列
# 先拿到 cancer 组的样本名列表
cancer_samples = sample_info[sample_info['分组'] == 'cancer']['样本名'].tolist()
print(f"\nCancer 组样本：{cancer_samples}")

# 选出基因名 + cancer 组的表达量
cancer_expr = gene_expression[['基因名'] + cancer_samples]
print("\n--- Cancer 组表达数据 ---")
print(cancer_expr)

# 场景 B：筛选在 sample_1 中高表达（> 20 TPM）的基因
high_expr = gene_expression[gene_expression['sample_1'] > 20]
print("\n--- sample_1 中表达量 > 20 TPM 的基因 ---")
print(high_expr)

# 场景 C：组合条件 — sample_1 > 10 且 sample_3 < 10
combined = gene_expression[
    (gene_expression['sample_1'] > 10) & (gene_expression['sample_3'] < 10)
]
print("\n--- sample_1 > 10 且 sample_3 < 10 的基因（癌症中上调？）---")
print(combined)


# ============================================================
# 4. 缺失值处理
# ============================================================
print("\n" + "=" * 60)
print("4. 缺失值处理")
print("=" * 60)

# 复制一份数据，人为制造缺失值（模拟实验中检测失败的情况）
df_missing = gene_expression.copy()
df_missing.loc[1, 'sample_2'] = np.nan  # BRCA1 在 sample_2 中检测失败
df_missing.loc[3, 'sample_4'] = np.nan  # EGFR 在 sample_4 中检测失败

print("\n--- 含缺失值的数据 ---")
print(df_missing)

# 查看每列有多少缺失值
print("\n--- 每列缺失值数量 ---")
print(df_missing.isnull().sum())

# 方法1：用该列的均值填充缺失值
df_filled = df_missing.copy()
for col in ['sample_1', 'sample_2', 'sample_3', 'sample_4']:
    df_filled[col] = df_filled[col].fillna(df_filled[col].mean())
print("\n--- 用列均值填充后 ---")
print(df_filled)

# 方法2：直接删除含缺失值的行
df_dropped = df_missing.dropna()
print("\n--- 删除含缺失值的行后 ---")
print(df_dropped)


# ============================================================
# 5. 分组统计（groupby）：比较 cancer vs normal
# ============================================================
print("\n" + "=" * 60)
print("5. 分组统计：cancer vs normal 平均表达量")
print("=" * 60)

# 思路：把表格从"宽格式"转为"长格式"，然后按分组统计
# 第一步：将样本列"融化"为长格式
df_long = gene_expression.melt(
    id_vars='基因名',               # 保持不变的列
    var_name='样本名',              # 原来的列名变成这一列的值
    value_name='表达量',            # 原来的值变成这一列
)
print("\n--- 长格式数据（前8行）---")
print(df_long.head(8))

# 第二步：合并分组信息
df_long = df_long.merge(sample_info, on='样本名')
print("\n--- 合并分组信息后（前8行）---")
print(df_long.head(8))

# 第三步：按 基因名 + 分组 计算平均表达量
group_mean = df_long.groupby(['基因名', '分组'])['表达量'].mean()
print("\n--- 每个基因在 cancer / normal 组的平均表达量 ---")
print(group_mean)

# 转为更易读的表格形式
group_mean_table = group_mean.unstack(fill_value=0)
print("\n--- 表格形式 ---")
print(group_mean_table)

# 计算 cancer / normal 的倍数变化（Fold Change）
group_mean_table['FC(cancer/normal)'] = (
    group_mean_table['cancer'] / group_mean_table['normal']
)
print("\n--- 加上倍数变化 ---")
print(group_mean_table.round(2))  # 保留2位小数


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("本次演示涵盖了：")
print("  1. 创建 DataFrame")
print("  2. head / shape / describe 等探索方法")
print("  3. 条件过滤（选列、选行、组合条件）")
print("  4. 缺失值检测、填充、删除")
print("  5. groupby 分组统计 + 倍数变化计算")
print("=" * 60)
