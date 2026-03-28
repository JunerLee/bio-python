"""
第5章 练习题：文件读写与异常处理
================================
共 2 道核心练习，请补全函数体中的代码。
运行此文件，如果输出与预期一致，说明你的实现正确。

本文件会先将示例 FASTA 数据写入临时文件，然后让你解析它。
"""

import os

# ============================================================
# 准备工作：创建示例 FASTA 文件供练习使用
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 示例 FASTA 数据：5条 DNA 序列（模拟从 NCBI 下载的基因片段）
SAMPLE_FASTA = """\
>Gene_A 假想蛋白基因
ATGCGTACGTACGATCGATCGTTAAGCGCTAGCTAGCTAGC
ATGCGTACGTTAAGCGCATGCGATCGATCGATCGATCGATC
>Gene_B 热休克蛋白基因
GGCCAATTGGCCAATTGGCC
>Gene_C 核糖体蛋白基因
ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG
ATCGATCGATCGATCGATCG
>Gene_D DNA修复酶基因
GCGCGCGCGCGCGCGCGCGCATATATATATATATAT
>Gene_E 转录因子基因
ATGAAATTTCCCGGGAAATTTCCCGGGAAATTTCCC
GGGAAATTTCCCGGGATGAAATTTCCCGGG
"""

# 将 FASTA 数据写入文件
fasta_path = os.path.join(SCRIPT_DIR, "exercise_sequences.fasta")
with open(fasta_path, "w") as f:
    f.write(SAMPLE_FASTA)
print(f"示例 FASTA 文件已创建: {fasta_path}\n")


# ============================================================
# 练习1：解析 FASTA 文件并统计序列信息
# ============================================================
#
# 【背景知识】
# 拿到一批序列后，第一步通常是做基本统计：
# 有多少条序列？最长的是哪条？GC含量如何？
# 这些信息能帮助你快速了解数据质量。
#
# 【任务】
# 完成下面三个函数：
#
# (1) parse_fasta(filepath)
#     - 读取 FASTA 文件，返回字典 {序列名: 序列内容}
#     - 序列名不包含开头的 >
#     - 多行序列要拼接成一个完整的字符串
#
# (2) calc_gc(seq)
#     - 计算一条 DNA 序列的 GC 含量百分比
#     - 返回 float，保留 2 位小数
#
# (3) analyze_fasta(filepath)
#     - 调用上面两个函数，返回一个字典，包含：
#       "序列数量": int
#       "最长序列名": str（最长序列的名称）
#       "最长序列长度": int
#       "平均GC含量": float（所有序列 GC 含量的平均值，保留 2 位小数）
#
# 【提示】
# - parse_fasta: 逐行读取，以 > 开头的是标题行，其余是序列行
# - calc_gc: (G个数 + C个数) / 总长度 * 100
# - analyze_fasta: 用 max() 找最长序列，用 sum()/len() 求平均值
#   提示：max() 可以搭配 key 参数使用
#         max(sequences, key=lambda name: len(sequences[name]))


def parse_fasta(filepath):
    """
    解析 FASTA 文件。

    参数:
        filepath: FASTA 文件路径

    返回:
        字典 {序列名: 序列字符串}

    示例:
        parse_fasta("seq.fasta")
        → {"Gene_A 假想蛋白基因": "ATGCGT...", "Gene_B ...": "GGCC..."}
    """
    sequences = {}
    current_name = None

    # ===== 请在下方编写你的代码 =====
    #
    # 提示步骤：
    # 1. 用 with open(filepath, "r") as f 打开文件
    # 2. 用 for line in f 逐行遍历
    # 3. 用 line.strip() 去掉换行符
    # 4. 如果 line.startswith(">")，提取序列名（去掉 >）
    # 5. 否则，把这一行拼接到当前序列上
    #

    pass  # ← 删除这行，替换为你的代码

    # ===== 代码结束 =====

    return sequences


def calc_gc(seq):
    """
    计算 DNA 序列的 GC 含量百分比。

    参数:
        seq: DNA 序列字符串（大写，仅含 A/T/G/C）

    返回:
        GC 含量百分比（float），保留 2 位小数

    示例:
        calc_gc("ATGCGCTA") → 50.0
    """
    # ===== 请在下方编写你的代码 =====
    #
    # 提示：
    # gc_count = seq.count("G") + seq.count("C")
    # 返回 round(gc_count / len(seq) * 100, 2)
    #

    pass  # ← 删除这行，替换为你的代码

    # ===== 代码结束 =====


def analyze_fasta(filepath):
    """
    对 FASTA 文件进行综合统计。

    参数:
        filepath: FASTA 文件路径

    返回:
        字典，包含以下键：
        - "序列数量": int
        - "最长序列名": str
        - "最长序列长度": int
        - "平均GC含量": float（保留 2 位小数）
    """
    # ===== 请在下方编写你的代码 =====
    #
    # 提示步骤：
    # 1. 调用 parse_fasta(filepath) 获取所有序列
    # 2. 序列数量 = len(sequences)
    # 3. 找最长序列：
    #    longest_name = max(sequences, key=lambda name: len(sequences[name]))
    #    longest_length = len(sequences[longest_name])
    # 4. 计算平均 GC 含量：
    #    gc_values = [calc_gc(seq) for seq in sequences.values()]
    #    avg_gc = round(sum(gc_values) / len(gc_values), 2)
    # 5. 返回结果字典
    #

    pass  # ← 删除这行，替换为你的代码

    # ===== 代码结束 =====


# —— 测试练习1 ——
print("=" * 55)
print("练习1：解析 FASTA 并统计序列信息")
print("=" * 55)

# 测试 parse_fasta
print("\n--- 测试 parse_fasta ---")
result_seqs = parse_fasta(fasta_path)

if result_seqs is None:
    print("  [提示] parse_fasta 返回了 None，请补全代码！")
else:
    expected_count = 5
    actual_count = len(result_seqs)
    status = "通过" if actual_count == expected_count else "未通过"
    print(f"  序列数量: 期望 {expected_count}, 实际 {actual_count} → [{status}]")

    # 检查 Gene_B 的序列长度（单行序列，便于验证）
    gene_b_key = "Gene_B 热休克蛋白基因"
    if gene_b_key in result_seqs:
        expected_len = 20
        actual_len = len(result_seqs[gene_b_key])
        status = "通过" if actual_len == expected_len else "未通过"
        print(f"  Gene_B 长度: 期望 {expected_len}, 实际 {actual_len} → [{status}]")

# 测试 calc_gc
print("\n--- 测试 calc_gc ---")
gc_test_cases = [
    ("ATGCGCTA", 50.0),
    ("AAATTTAA", 0.0),
    ("GCGCGCGC", 100.0),
]

for seq, expected_gc in gc_test_cases:
    result_gc = calc_gc(seq)
    if result_gc is None:
        print(f"  [提示] calc_gc 返回了 None，请补全代码！")
        break
    status = "通过" if result_gc == expected_gc else "未通过"
    print(f"  {seq} → 期望 {expected_gc}%, 实际 {result_gc}% → [{status}]")

# 测试 analyze_fasta
print("\n--- 测试 analyze_fasta ---")
stats = analyze_fasta(fasta_path)

if stats is None:
    print("  [提示] analyze_fasta 返回了 None，请补全代码！")
else:
    expected_stats = {
        "序列数量": 5,
        "最长序列名": "Gene_A 假想蛋白基因",
        "最长序列长度": 82,
    }
    for key, expected_val in expected_stats.items():
        actual_val = stats.get(key)
        status = "通过" if actual_val == expected_val else "未通过"
        print(f"  {key}: 期望 {expected_val}, 实际 {actual_val} → [{status}]")

    # GC含量单独检查（允许浮点误差）
    avg_gc = stats.get("平均GC含量")
    if avg_gc is not None:
        print(f"  平均GC含量: {avg_gc}%")

print()


# ============================================================
# 练习2：将统计结果保存为文本报告
# ============================================================
#
# 【背景知识】
# 做完数据分析后，要把结果保存下来——这是科研的基本素养。
# 这道练习让你把分析结果写入一个格式清晰的文本文件。
#
# 【任务】
# 完成函数 save_report(stats, sequences, output_path):
# - stats 是 analyze_fasta() 的返回值（字典）
# - sequences 是 parse_fasta() 的返回值（字典）
# - output_path 是输出文件的路径
#
# 输出的文本文件格式如下：
# ==============================
# FASTA 序列分析报告
# ==============================
# 序列数量: 5
# 最长序列: Gene_A 假想蛋白基因 (82 bp)
# 平均GC含量: xx.xx%
#
# --- 各序列详情 ---
# Gene_A 假想蛋白基因: 82 bp, GC=xx.xx%
# Gene_B 热休克蛋白基因: 20 bp, GC=xx.xx%
# ...
#
# 【提示】
# - 用 with open(output_path, "w") as f 打开文件
# - 用 f.write("内容\n") 写入每一行（别忘了 \n 换行）
# - 可以用 f-string 格式化：f"序列数量: {stats['序列数量']}\n"


def save_report(stats, sequences, output_path):
    """
    将分析结果保存为文本报告。

    参数:
        stats: analyze_fasta() 返回的统计字典
        sequences: parse_fasta() 返回的 {序列名: 序列} 字典
        output_path: 输出文件路径
    """
    # ===== 请在下方编写你的代码 =====
    #
    # 提示步骤：
    # 1. 用 with open(output_path, "w") as f 打开文件
    # 2. 写入报告标题（用 = 号做分隔线）
    # 3. 写入 stats 中的汇总信息
    # 4. 写入分隔线
    # 5. 遍历 sequences，写入每条序列的名称、长度和 GC 含量
    #    提示：用 calc_gc(seq) 计算每条序列的 GC 含量
    #

    pass  # ← 删除这行，替换为你的代码

    # ===== 代码结束 =====


# —— 测试练习2 ——
print("=" * 55)
print("练习2：保存分析报告")
print("=" * 55)

report_path = os.path.join(SCRIPT_DIR, "analysis_report.txt")

# 只有在练习1完成后才能测试练习2
if result_seqs is not None and stats is not None:
    try:
        save_report(stats, result_seqs, report_path)

        # 验证文件是否创建成功
        if os.path.exists(report_path):
            print(f"  报告文件已创建: {report_path}")
            print("\n  --- 报告内容预览 ---")
            with open(report_path, "r") as f:
                content = f.read()
            if content.strip():
                # 只显示前10行
                lines = content.split("\n")
                for line in lines[:10]:
                    print(f"  {line}")
                if len(lines) > 10:
                    print(f"  ... (共 {len(lines)} 行)")
                print(f"\n  → [通过] 报告保存成功！")
            else:
                print("  → [未通过] 报告文件为空，请补全 save_report 函数！")
        else:
            print("  → [未通过] 报告文件未创建，请补全 save_report 函数！")
    except Exception as e:
        print(f"  → [错误] {e}")
else:
    print("  [提示] 请先完成练习1，再测试练习2。")

print()
print("完成所有练习后，所有测试应显示【通过】。加油！")
