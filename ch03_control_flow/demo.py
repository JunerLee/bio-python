"""
第3章 代码演示：条件判断与循环
================================
通过生物信息学实例，演示 if/elif/else、for 循环、列表推导式等核心语法。
"""

# ============================================================
# 1. 条件判断：判断碱基类型（嘌呤 vs 嘧啶）
# ============================================================
# 嘌呤（Purine）：A, G —— 双环结构
# 嘧啶（Pyrimidine）：C, T, U —— 单环结构

base = "G"

if base in ("A", "G"):
    print(f"{base} 是嘌呤（Purine）")
elif base in ("C", "T", "U"):
    print(f"{base} 是嘧啶（Pyrimidine）")
else:
    print(f"{base} 不是标准碱基")

# ============================================================
# 2. for 循环：计算 DNA 序列的 GC 含量
# ============================================================
# GC 含量 = (G 的个数 + C 的个数) / 序列总长度
# GC 含量是衡量 DNA 稳定性的重要指标（GC 含量越高，双链越稳定）

dna_seq = "ATGCGCTATGCAATCGGCTAAGC"
print(f"\nDNA 序列：{dna_seq}")

# --- 方法：用 for 循环逐个碱基统计 ---
gc_count = 0  # 用于累计 G 和 C 的个数

for base in dna_seq:
    if base == "G" or base == "C":
        gc_count += 1  # 等价于 gc_count = gc_count + 1

gc_content = gc_count / len(dna_seq)
print(f"GC 含量：{gc_content:.2%}")  # :.2% 表示格式化为百分比，保留2位小数

# ============================================================
# 3. enumerate()：带位置信息地遍历序列
# ============================================================
# 找出序列中所有 G 碱基的位置

print(f"\n在序列中查找 G 碱基的位置：")

for position, base in enumerate(dna_seq):
    if base == "G":
        print(f"  位置 {position}: {base}")

# ============================================================
# 4. for 循环 + 条件：遍历基因列表，筛选长序列
# ============================================================
# 假设我们有一批基因序列，需要筛选出长度 > 100 bp 的序列

gene_sequences = {
    "BRCA1": "ATGCGA" * 20,    # 120 bp
    "TP53":  "GCTATC" * 15,    # 90 bp
    "EGFR":  "ATCGGC" * 25,    # 150 bp
    "MYC":   "TAGCTA" * 10,    # 60 bp
}

print("\n筛选长度 > 100 bp 的基因序列：")
print("-" * 35)

long_genes = []  # 用于存放筛选结果

for gene_name, sequence in gene_sequences.items():
    seq_length = len(sequence)

    if seq_length > 100:
        print(f"  ✅ {gene_name}: {seq_length} bp")
        long_genes.append(gene_name)
    else:
        print(f"  ❌ {gene_name}: {seq_length} bp（太短，跳过）")

print(f"\n符合条件的基因：{long_genes}")

# ============================================================
# 5. 列表推导式：生成互补碱基序列
# ============================================================
# DNA 互补配对规则：A-T, T-A, G-C, C-G

# 先定义一个互补配对的字典
complement_map = {"A": "T", "T": "A", "G": "C", "C": "G"}

dna = "ATGCGA"

# --- 传统写法 ---
comp_traditional = []
for base in dna:
    comp_traditional.append(complement_map[base])
print(f"\n原始序列：    {dna}")
print(f"互补序列（传统）：{''.join(comp_traditional)}")

# --- 列表推导式：一行搞定 ---
comp_list = [complement_map[b] for b in dna]
comp_seq = "".join(comp_list)  # 把列表拼成字符串
print(f"互补序列（推导式）：{comp_seq}")

# ============================================================
# 6. 列表推导式 + 条件过滤：提取 GC 碱基
# ============================================================

seq = "ATGCGCTATGCAAT"

# 只保留 G 和 C
gc_bases = [b for b in seq if b in "GC"]
print(f"\n序列 {seq} 中的 GC 碱基：{gc_bases}")
print(f"GC 碱基个数：{len(gc_bases)}")

# ============================================================
# 7. while 循环：模拟 PCR 扩增
# ============================================================
# PCR 每个循环使 DNA 分子数翻倍

molecules = 1       # 初始 1 个 DNA 分子
cycle = 0
target = 1000       # 目标：至少 1000 个分子

print(f"\n模拟 PCR 扩增（目标：>= {target} 个分子）：")

while molecules < target:
    molecules *= 2   # 每轮翻倍
    cycle += 1

print(f"  经过 {cycle} 轮循环，DNA 分子数达到 {molecules}")

# ============================================================
# 8. break 和 continue 示例
# ============================================================

# break：在 mRNA 序列中找到第一个终止密码子后停止
mrna = "AUGGCUUAAGGA"

# 每3个碱基为一个密码子
print(f"\n翻译 mRNA 序列：{mrna}")
stop_codons = {"UAA", "UAG", "UGA"}

for i in range(0, len(mrna), 3):       # 步长为3，每次取3个碱基
    codon = mrna[i:i+3]

    if codon in stop_codons:
        print(f"  密码子 {codon} → ⛔ 终止！翻译结束")
        break
    else:
        print(f"  密码子 {codon} → 翻译中...")

# continue：清洗序列中的无效碱基 N
raw_seq = "ATNGCNNATG"
clean_seq = ""

for base in raw_seq:
    if base == "N":
        continue  # 跳过 N，不执行下面的拼接
    clean_seq += base

print(f"\n原始序列：{raw_seq}")
print(f"清洗后：  {clean_seq}")
