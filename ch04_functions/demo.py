"""
第4章 代码演示：函数与模块
=========================
本文件演示如何定义和使用函数，以及导入标准库模块。
所有示例均围绕生物学场景展开。
"""

# ============================================================
# 第1部分：计算 GC 含量的函数
# ============================================================
# GC 含量 = (G + C) / 序列总长度 × 100%
# GC 含量是衡量 DNA 序列特性的重要指标，
# 例如高 GC 含量区域通常更稳定（因为 G-C 之间有三条氢键）。

def calc_gc(seq, round_digits=2):
    """
    计算 DNA 序列的 GC 含量。

    参数:
        seq: DNA 序列字符串，仅含 A/T/G/C（大写）
        round_digits: 保留小数位数，默认 2

    返回:
        GC 含量百分比（float），例如 50.0 表示 50%
    """
    # 统计 G 和 C 的个数，除以总长度，再乘 100 得到百分比
    gc_count = seq.count("G") + seq.count("C")
    gc_percent = gc_count / len(seq) * 100
    return round(gc_percent, round_digits)


# —— 测试一下 ——
print("=" * 50)
print("【1】计算 GC 含量")
print("=" * 50)

test_sequences = {
    "序列A": "ATGCGCTA",
    "序列B": "AAATTTAA",
    "序列C": "GCGCGCGC",
}

for name, seq in test_sequences.items():
    gc = calc_gc(seq)
    print(f"  {name}: {seq} → GC含量 = {gc}%")

print()


# ============================================================
# 第2部分：生成互补链的函数
# ============================================================
# DNA 碱基互补配对规则：A↔T, G↔C
# 例如：5'-ATGC-3' 的互补链是 3'-TACG-5'

def complement(seq):
    """
    生成 DNA 序列的互补链。

    参数:
        seq: DNA 序列字符串（大写，仅含 A/T/G/C）

    返回:
        互补链字符串
    """
    # 定义碱基互补配对的映射字典
    base_pair = {
        "A": "T",
        "T": "A",
        "G": "C",
        "C": "G",
    }

    # 逐个碱基转换，拼接成互补链
    comp_seq = ""
    for base in seq:
        comp_seq += base_pair[base]

    return comp_seq


def reverse_complement(seq):
    """
    生成 DNA 序列的反向互补链。

    在实际生物学中，双链 DNA 的两条链方向相反（5'→3' 和 3'→5'），
    所以反向互补链 = 先互补，再反转。

    参数:
        seq: DNA 序列字符串

    返回:
        反向互补链字符串
    """
    # 先求互补链，再用切片 [::-1] 反转
    return complement(seq)[::-1]


# —— 测试一下 ——
print("=" * 50)
print("【2】生成互补链 / 反向互补链")
print("=" * 50)

dna = "ATGCGCTA"
print(f"  原始序列:     5'-{dna}-3'")
print(f"  互补链:       3'-{complement(dna)}-5'")
print(f"  反向互补链:   5'-{reverse_complement(dna)}-3'")
print()


# ============================================================
# 第3部分：使用 random 模块模拟基因突变
# ============================================================
# 点突变：DNA 序列中某个碱基被随机替换为另一个碱基。
# 这里用 random 模块来模拟这个随机过程。

import random  # 导入随机数模块——"随机数仪器柜"

def mutate(seq, mutation_rate=0.05, seed=None):
    """
    模拟 DNA 序列的随机点突变。

    参数:
        seq: 原始 DNA 序列
        mutation_rate: 每个碱基发生突变的概率，默认 5%
        seed: 随机数种子，设定后结果可复现（方便教学演示）

    返回:
        突变后的序列字符串
    """
    if seed is not None:
        random.seed(seed)  # 设置随机种子，确保结果可复现

    bases = ["A", "T", "G", "C"]
    mutated = ""
    mutation_count = 0

    for base in seq:
        # random.random() 返回 0~1 之间的随机小数
        if random.random() < mutation_rate:
            # 发生突变：从其他三种碱基中随机选一个
            other_bases = [b for b in bases if b != base]
            new_base = random.choice(other_bases)
            mutated += new_base
            mutation_count += 1
        else:
            # 不突变：保留原碱基
            mutated += base

    print(f"  共发生 {mutation_count} 个点突变（突变率 {mutation_rate*100}%）")
    return mutated


# —— 测试一下 ——
print("=" * 50)
print("【3】模拟基因突变（使用 random 模块）")
print("=" * 50)

original = "ATGCGCTAATGCGCTAATGCGCTA"  # 24 个碱基
print(f"  原始序列: {original}")
result = mutate(original, mutation_rate=0.1, seed=42)
print(f"  突变序列: {result}")

# 标记突变位置
diff = ""
for o, m in zip(original, result):
    diff += "^" if o != m else " "
print(f"  突变位置: {diff}")
print()


# ============================================================
# 第4部分：使用 import math 演示数学模块
# ============================================================
# math 模块提供常用数学函数和常量

import math  # 导入数学模块——"数学运算仪器柜"

print("=" * 50)
print("【4】math 模块演示")
print("=" * 50)

# 计算 log2（在基因表达分析中经常使用 log2 fold change）
expression_a = 100  # 条件 A 的基因表达量
expression_b = 400  # 条件 B 的基因表达量
log2_fc = math.log2(expression_b / expression_a)
print(f"  表达量 A={expression_a}, B={expression_b}")
print(f"  log2(Fold Change) = {log2_fc}")

# 计算平方根（例如标准差计算中会用到）
variance = 25.0
std_dev = math.sqrt(variance)
print(f"  方差={variance}, 标准差={std_dev}")

# 常量
print(f"  圆周率 π = {math.pi}")
print(f"  自然常数 e = {math.e}")
print()


# ============================================================
# 第5部分：函数组合 —— 综合分析一条 DNA 序列
# ============================================================
# 一个函数可以调用其他函数，就像一个完整的实验流程调用多个子步骤。

def analyze_sequence(seq):
    """
    对一条 DNA 序列进行综合分析。

    参数:
        seq: DNA 序列字符串

    返回:
        包含分析结果的字典
    """
    return {
        "序列长度": len(seq),
        "GC含量(%)": calc_gc(seq),
        "互补链": complement(seq),
        "反向互补链": reverse_complement(seq),
    }


print("=" * 50)
print("【5】综合分析（函数组合调用）")
print("=" * 50)

seq = "ATGCGTACGTTAGC"
print(f"  待分析序列: {seq}")
result = analyze_sequence(seq)

for key, value in result.items():
    print(f"  {key}: {value}")

print()
print("演示结束！")
