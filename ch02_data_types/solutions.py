"""
第2章 练习题：数据类型与数据结构
=================================
运行方式：uv run python ch02_data_types/solutions.py

本文件已补全参考答案。
运行后可对照输出，检查每一步是否符合预期。

前置知识：
- 基本数据类型（int, float, str, bool）
- 字符串操作（len, count, replace, 切片）
- 列表（list）和字典（dict）
"""


# ============================================================
# 练习1：DNA 碱基统计
# ============================================================
#
# 任务：给定一条 DNA 序列，统计其中 A、T、C、G 各出现了多少次，
#       并计算 GC 含量（G和C的数量之和 / 总长度）。
#
# 预期输出（大致格式）：
#   DNA 序列: ATCGATCGAATTCCGG
#   序列长度: 16
#   A: 4, T: 4, C: 4, G: 4
#   GC 含量: 0.5
#
# 提示：
#   - 用 len() 获取序列长度
#   - 用 str.count() 统计某个字符出现的次数
#   - GC 含量 = (G的数量 + C的数量) / 序列总长度
# ============================================================

print("=== 练习1：DNA 碱基统计 ===")

dna_seq = "ATCGATCGAATTCCGG"

# 第1步：打印 DNA 序列和序列长度
seq_length = len(dna_seq)
print("DNA 序列:", dna_seq)
print("序列长度:", seq_length)

# 第2步：分别统计 A、T、C、G 的数量
a_count = dna_seq.count("A")
t_count = dna_seq.count("T")
c_count = dna_seq.count("C")
g_count = dna_seq.count("G")
print(f"A: {a_count}, T: {t_count}, C: {c_count}, G: {g_count}")

# 第3步：计算 GC 含量并打印
gc_content = (g_count + c_count) / seq_length
print("GC 含量:", gc_content)

print()


# ============================================================
# 练习2：构建密码子-氨基酸字典
# ============================================================
#
# 任务：
#   (1) 创建一个字典，包含以下密码子和对应的氨基酸：
#       AUG → Met
#       UUU → Phe
#       GAA → Glu
#       GCU → Ala
#       UAA → Stop
#
#   (2) 给定一条 mRNA 片段 "AUGUUUGAAGCUUAA"，
#       将它按每3个碱基分割成密码子，
#       然后用字典查找每个密码子对应的氨基酸并打印。
#
# 预期输出（大致格式）：
#   AUG → Met
#   UUU → Phe
#   GAA → Glu
#   GCU → Ala
#   UAA → Stop
#
# 提示：
#   - 创建字典：my_dict = {"键": "值", ...}
#   - 字符串切片提取每3个碱基：mRNA[0:3], mRNA[3:6], mRNA[6:9], ...
#   - 用 dict[key] 或 dict.get(key, 默认值) 查找
#   - 本练习的 mRNA 只有 5 个密码子（15个碱基），手动切片 5 次即可
#   - （进阶，学完第3章后再试）用 for + range(0, len(mRNA), 3) 可以自动化
# ============================================================

print("=== 练习2：构建密码子-氨基酸字典 ===")

mrna = "AUGUUUGAAGCUUAA"

# 第1步：创建密码子字典
codon_table = {
    "AUG": "Met",
    "UUU": "Phe",
    "GAA": "Glu",
    "GCU": "Ala",
    "UAA": "Stop",
}

# 第2步：逐个切片取出密码子，查字典并打印
codon_1 = mrna[0:3]
codon_2 = mrna[3:6]
codon_3 = mrna[6:9]
codon_4 = mrna[9:12]
codon_5 = mrna[12:15]

print(f"{codon_1} → {codon_table[codon_1]}")
print(f"{codon_2} → {codon_table[codon_2]}")
print(f"{codon_3} → {codon_table[codon_3]}")
print(f"{codon_4} → {codon_table[codon_4]}")
print(f"{codon_5} → {codon_table[codon_5]}")

print()


# ============================================================
# 练习3（挑战题）：DNA 互补链生成
# ============================================================
#
# 任务：给定一条 DNA 正义链，生成它的互补链。
#
# 互补规则：A ↔ T，C ↔ G
#
# 示例：
#   正义链:  ATCGATCG
#   互补链:  TAGCTAGC
#
# 预期输出：
#   正义链: ATCGATCG
#   互补链: TAGCTAGC
#
# 提示：
#   - 可以用多次 replace() 实现，但要注意替换顺序的陷阱！
#     如果先把 A 替换成 T，再把 T 替换成 A，之前替换的 T 又会变回 A。
#   - 一种解决思路：先全部转小写做替换，最后再转大写。
#     例如：先 replace("A", "t")，再 replace("T", "a")……最后 upper()
#   - 还有其他思路，比如遍历每个碱基，用字典查找互补碱基。
# ============================================================

print("=== 练习3（挑战题）：DNA 互补链生成 ===")

sense_strand = "ATCGATCG"

complement_strand = (
    sense_strand
    .replace("A", "t")
    .replace("T", "a")
    .replace("C", "g")
    .replace("G", "c")
    .upper()
)

print("正义链:", sense_strand)
print("互补链:", complement_strand)

print()
