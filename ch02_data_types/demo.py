"""
第2章 演示代码：数据类型与数据结构
===================================
运行方式：uv run python ch02_data_types/demo.py

本文件演示 Python 中常用的数据类型和数据结构，
所有示例均以生物信息学场景为背景。
"""

# ============================================================
# 第1部分：基本数据类型
# ============================================================

# --- 整数 int ---
# 适合表示"可以数出来"的量

chromosome_num = 23                # 人类单倍体染色体数目
base_pairs = 3_200_000_000         # 人类基因组大约有32亿个碱基对

print("=== 整数 int ===")
print(f"人类染色体数目: {chromosome_num}")
print(f"基因组碱基对数: {base_pairs}")
print(f"类型: {type(chromosome_num)}")
print()

# --- 浮点数 float ---
# 适合表示带小数的测量值

ph_value = 7.4          # 人体血液 pH 值
gc_content = 0.42        # 某段 DNA 的 GC 含量（42%）
enzyme_activity = 3.5e2  # 酶活性，科学计数法表示 350.0

print("=== 浮点数 float ===")
print(f"血液 pH: {ph_value}")
print(f"GC 含量: {gc_content}")
print(f"酶活性: {enzyme_activity}")
print(f"注意精度: 0.1 + 0.2 = {0.1 + 0.2}")
print()

# --- 布尔值 bool ---
# 只有 True 和 False 两个值

is_expressed = True      # 这个基因是否在该组织中表达
is_mutated = False       # 是否检测到突变

print("=== 布尔值 bool ===")
print(f"基因是否表达: {is_expressed}")
print(f"是否突变: {is_mutated}")
print(f"类型: {type(is_expressed)}")
print()


# ============================================================
# 第2部分：字符串 str —— 处理 DNA/RNA 序列的核心工具 ⭐
# ============================================================

print("=== 字符串 str ===")

dna = "ATCGATCGATCG"
gene = "TP53"

# --- 基本信息 ---
print(f"DNA 序列: {dna}")
print(f"序列长度: {len(dna)} bp")
print(f"基因名: {gene}")
print()

# --- 拼接与重复 ---
fragment1 = "ATCG"
fragment2 = "TTAA"
joined = fragment1 + fragment2         # 拼接两段序列
print(f"序列拼接: {fragment1} + {fragment2} = {joined}")
print(f"重复序列: {'AT' * 5} = {'AT' * 5}")
print()

# --- 大小写转换 ---
mixed_case = "AtCgTa"
print(f"原始: {mixed_case}")
print(f"转大写 upper(): {mixed_case.upper()}")
print(f"转小写 lower(): {mixed_case.lower()}")
print()

# --- 统计与查找 ---
print(f"序列: {dna}")
print(f"A 的数量 count('A'): {dna.count('A')}")
print(f"G 的数量 count('G'): {dna.count('G')}")
print(f"查找 'GAT' 的位置 find(): {dna.find('GAT')}")
print(f"查找 'XXX'（不存在）: {dna.find('XXX')}")  # 找不到返回 -1
print()

# --- 替换：DNA → RNA 转录 ---
rna = dna.replace("T", "U")
print(f"DNA: {dna}")
print(f"RNA（T→U）: {rna}")
print()

# --- 字符串切片：提取子序列 ---
#
#  索引:  0   1   2   3   4   5   6   7   8   9  10  11
#  碱基:  A   T   C   G   A   T   C   G   A   T   C   G
# 负索引:-12 -11 -10  -9  -8  -7  -6  -5  -4  -3  -2  -1

print(f"序列: {dna}")
print(f"第一个碱基 dna[0]: {dna[0]}")
print(f"最后一个碱基 dna[-1]: {dna[-1]}")
print(f"前4个碱基 dna[:4]: {dna[:4]}")
print(f"第3到第6个碱基 dna[2:6]: {dna[2:6]}")
print(f"最后3个碱基 dna[-3:]: {dna[-3:]}")
print(f"反转序列 dna[::-1]: {dna[::-1]}")
print(f"每隔一个取 dna[::2]: {dna[::2]}")
print()


# ============================================================
# 第3部分：类型查看与类型转换
# ============================================================

print("=== 类型查看与转换 ===")

# type() 查看类型
print(f"type(23) = {type(23)}")
print(f"type(7.4) = {type(7.4)}")
print(f"type('ATCG') = {type('ATCG')}")
print(f"type(True) = {type(True)}")
print()

# 类型转换：从文件读取的数据通常是字符串，需要转成数字
position_str = "12345"                 # 这是一个字符串
position_int = int(position_str)       # 转成整数
print(f"字符串 '{position_str}' → 整数 {position_int}，类型: {type(position_int)}")

gc_str = "0.42"
gc_float = float(gc_str)              # 字符串转浮点数
print(f"字符串 '{gc_str}' → 浮点数 {gc_float}，类型: {type(gc_float)}")

num = 23
num_str = str(num)                     # 整数转字符串
print(f"整数 {num} → 字符串 '{num_str}'，类型: {type(num_str)}")
print()


# ============================================================
# 第4部分：列表 list —— 管理一组数据 ⭐
# ============================================================

print("=== 列表 list ===")

# 创建一个基因列表
genes = ["TP53", "BRCA1", "EGFR", "MYC", "KRAS"]
print(f"基因列表: {genes}")
print(f"列表长度: {len(genes)}")
print()

# --- 索引和切片（规则与字符串相同）---
print(f"第一个基因 genes[0]: {genes[0]}")
print(f"最后一个基因 genes[-1]: {genes[-1]}")
print(f"前三个基因 genes[:3]: {genes[:3]}")
print()

# --- 修改元素（列表是可变的！）---
print(f"修改前: {genes}")
genes[0] = "TP53_mutant"              # 将第一个基因标记为突变型
print(f"修改后: {genes}")
genes[0] = "TP53"                     # 改回来
print()

# --- 添加和删除 ---
genes.append("PTEN")                  # 在末尾添加一个基因
print(f"append('PTEN') 后: {genes}")

removed = genes.pop()                 # 删除并返回最后一个元素
print(f"pop() 删除了: {removed}")
print(f"pop() 后: {genes}")
print()

# --- 排序 ---
expression_levels = [5.2, 1.3, 8.7, 3.1, 6.4]
print(f"排序前: {expression_levels}")
expression_levels.sort()               # 原地排序（从小到大）
print(f"排序后: {expression_levels}")
expression_levels.sort(reverse=True)   # 从大到小
print(f"降序排列: {expression_levels}")
print()

# --- 成员检测 ---
print(f"'BRCA1' 在列表中吗？ {'BRCA1' in genes}")
print(f"'ABCD' 在列表中吗？ {'ABCD' in genes}")
print()


# ============================================================
# 第5部分：字典 dict —— 键值对映射 ⭐
# ============================================================

print("=== 字典 dict ===")

# 创建一个简化的密码子表
codon_table = {
    "AUG": "Met (甲硫氨酸 / 起始密码子)",
    "UUU": "Phe (苯丙氨酸)",
    "UUC": "Phe (苯丙氨酸)",
    "GAA": "Glu (谷氨酸)",
    "UAA": "Stop (终止)",
}

print(f"密码子表: {codon_table}")
print(f"密码子数量: {len(codon_table)}")
print()

# --- 通过键取值 ---
print(f"AUG 编码: {codon_table['AUG']}")
print(f"UUU 编码: {codon_table['UUU']}")
print()

# --- 安全取值：get() ---
# 键不存在时不会报错，而是返回默认值
result = codon_table.get("XXX", "未知密码子")
print(f"查找 'XXX': {result}")
print()

# --- 添加新键值对 ---
codon_table["GCU"] = "Ala (丙氨酸)"
print(f"添加 GCU 后: {codon_table}")
print()

# --- 遍历字典 ---
print("遍历密码子表:")
for codon, amino_acid in codon_table.items():
    print(f"  {codon} → {amino_acid}")
print()

# --- 获取所有键和所有值 ---
print(f"所有密码子（键）: {list(codon_table.keys())}")
print(f"所有氨基酸（值）: {list(codon_table.values())}")
print()


# ============================================================
# 第6部分：元组 tuple —— 不可变的有序数据
# ============================================================

print("=== 元组 tuple ===")

# 基因组坐标通常用元组表示：(染色体, 起始位置, 终止位置)
coordinate = ("chr1", 11345, 22345)
print(f"基因坐标: {coordinate}")
print(f"染色体: {coordinate[0]}")
print(f"起始位置: {coordinate[1]}")
print(f"终止位置: {coordinate[2]}")
print()

# 元组不可修改
# coordinate[0] = "chr2"  # ❌ 取消注释会报 TypeError

# 元组解包：把元组的值一次性赋给多个变量
chrom, start, end = coordinate
print(f"解包结果 → 染色体: {chrom}, 起始: {start}, 终止: {end}")
print()


# ============================================================
# 总结
# ============================================================

print("=" * 50)
print("本章核心知识点:")
print("  1. 基本类型: int, float, str, bool")
print("  2. 字符串操作: 切片、拼接、count/replace/find")
print("  3. 列表 list: 有序、可变，用索引访问")
print("  4. 字典 dict: 键值对，用键访问")
print("  5. 元组 tuple: 有序、不可变")
print("  6. 类型转换: int(), float(), str()")
print("=" * 50)
