"""
第4章 练习题：函数与模块
========================
共 2 道核心练习，下面给出参考答案。
运行此文件，如果输出与预期一致，说明实现正确。
"""

# ============================================================
# 练习1：将 DNA 翻译为蛋白质
# ============================================================
#
# 【背景知识】
# 中心法则：DNA → mRNA → 蛋白质
# 翻译过程中，每 3 个碱基（密码子）对应一个氨基酸。
# 起始密码子 ATG 编码甲硫氨酸（M），
# 终止密码子 TAA/TAG/TGA 不编码氨基酸，翻译停止。
#
# 【任务】
# 编写函数 translate(dna_seq)，将 DNA 序列翻译为蛋白质序列。
# - 从头开始，每 3 个碱基查一次密码子表
# - 遇到终止密码子就停止翻译
# - 返回蛋白质序列字符串
#
# 【提示】
# - 用 range(0, len(seq), 3) 可以每次跳 3 个位置
# - 用切片 seq[i:i+3] 可以取出 3 个碱基
# - 终止密码子在表中用 "*" 表示，遇到 "*" 时 break 跳出循环

# 简化版密码子表（仅包含部分密码子，足够完成练习）
CODON_TABLE = {
    "ATG": "M",  # 甲硫氨酸（起始密码子）
    "TTT": "F",  "TTC": "F",  # 苯丙氨酸
    "TTA": "L",  "TTG": "L",  # 亮氨酸
    "CTT": "L",  "CTC": "L",  "CTA": "L",  "CTG": "L",
    "ATT": "I",  "ATC": "I",  "ATA": "I",  # 异亮氨酸
    "GTT": "V",  "GTC": "V",  "GTA": "V",  "GTG": "V",  # 缬氨酸
    "TCT": "S",  "TCC": "S",  "TCA": "S",  "TCG": "S",  # 丝氨酸
    "CCT": "P",  "CCC": "P",  "CCA": "P",  "CCG": "P",  # 脯氨酸
    "ACT": "T",  "ACC": "T",  "ACA": "T",  "ACG": "T",  # 苏氨酸
    "GCT": "A",  "GCC": "A",  "GCA": "A",  "GCG": "A",  # 丙氨酸
    "TAT": "Y",  "TAC": "Y",  # 酪氨酸
    "CAT": "H",  "CAC": "H",  # 组氨酸
    "CAA": "Q",  "CAG": "Q",  # 谷氨酰胺
    "AAT": "N",  "AAC": "N",  # 天冬酰胺
    "AAA": "K",  "AAG": "K",  # 赖氨酸
    "GAT": "D",  "GAC": "D",  # 天冬氨酸
    "GAA": "E",  "GAG": "E",  # 谷氨酸
    "TGT": "C",  "TGC": "C",  # 半胱氨酸
    "TGG": "W",                # 色氨酸
    "CGT": "R",  "CGC": "R",  "CGA": "R",  "CGG": "R",  # 精氨酸
    "AGT": "S",  "AGC": "S",  # 丝氨酸
    "AGA": "R",  "AGG": "R",  # 精氨酸
    "GGT": "G",  "GGC": "G",  "GGA": "G",  "GGG": "G",  # 甘氨酸
    # 终止密码子
    "TAA": "*",  "TAG": "*",  "TGA": "*",
}


def translate(dna_seq):
    """
    将 DNA 序列翻译为蛋白质序列。

    参数:
        dna_seq: DNA 序列字符串（长度应为 3 的倍数）

    返回:
        蛋白质序列字符串（单字母氨基酸代码）

    示例:
        translate("ATGTTTTAA") → "MF"
        （ATG=M, TTT=F, TAA=终止）
    """
    protein = ""

    for i in range(0, len(dna_seq), 3):
        codon = dna_seq[i:i + 3]
        if len(codon) < 3:
            break

        amino_acid = CODON_TABLE[codon]
        if amino_acid == "*":
            break

        protein += amino_acid

    return protein


# —— 测试你的函数 ——
print("=" * 50)
print("练习1：DNA 翻译为蛋白质")
print("=" * 50)

test_cases = [
    ("ATGTTTTAA", "MF"),            # ATG=M, TTT=F, TAA=终止
    ("ATGGCGAATTGA", "MAN"),        # ATG=M, GCG=A, AAT=N, TGA=终止
    ("ATGTGGTATTAG", "MWY"),        # ATG=M, TGG=W, TAT=Y, TAG=终止
]

for dna, expected in test_cases:
    result = translate(dna)
    status = "通过" if result == expected else "未通过"
    print(f"  输入: {dna}")
    print(f"  期望: {expected}, 你的结果: {result} → [{status}]")
    print()


# ============================================================
# 练习2：计算两条序列的相似度
# ============================================================
#
# 【背景知识】
# 序列比对是生物信息学的基础操作之一。
# 最简单的比对方式：逐个位置比较两条等长序列，
# 相同位置碱基一致的比例就是"序列相似度"。
#
# 例如：
#   序列1: A T G C G C
#   序列2: A T A C G C
#   比较:  = = x = = =    → 5/6 匹配 → 相似度 83.33%
#
# 【任务】
# 编写函数 similarity(seq1, seq2)，计算两条等长序列的相似度。
# - 逐个位置比较两条序列
# - 返回相似度百分比（float）
#
# 【提示】
# - 可以用 zip(seq1, seq2) 同时遍历两条序列
#   for base1, base2 in zip(seq1, seq2):
#       ...
# - 统计匹配的位置数，除以总长度，乘以 100


def similarity(seq1, seq2):
    """
    计算两条等长 DNA 序列的相似度（逐位比对）。

    参数:
        seq1: 第一条 DNA 序列
        seq2: 第二条 DNA 序列（与 seq1 等长）

    返回:
        相似度百分比（float），保留 2 位小数

    示例:
        similarity("ATGCGC", "ATACGC") → 83.33
    """
    match_count = 0

    if len(seq1) != len(seq2):
        raise ValueError("两条序列长度必须相同")

    for base1, base2 in zip(seq1, seq2):
        if base1 == base2:
            match_count += 1

    return round(match_count / len(seq1) * 100, 2)


# —— 测试你的函数 ——
print("=" * 50)
print("练习2：计算序列相似度")
print("=" * 50)

test_cases_2 = [
    ("ATGCGC", "ATACGC", 83.33),     # 5/6 匹配
    ("AAAA", "AAAA", 100.0),          # 完全一致
    ("ATGC", "TACG", 0.0),            # 完全不同
    ("ATGCATGC", "ATGGATGC", 87.5),   # 7/8 匹配
]

for s1, s2, expected in test_cases_2:
    result = similarity(s1, s2)
    status = "通过" if result == expected else "未通过"
    print(f"  序列1: {s1}")
    print(f"  序列2: {s2}")
    print(f"  期望: {expected}%, 你的结果: {result}% → [{status}]")
    print()

print("完成所有练习后，所有测试应显示【通过】。加油！")
