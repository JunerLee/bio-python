"""
第5章 代码演示：文件读写与异常处理
===================================
本文件演示如何读写文件、解析 FASTA 格式、输出 CSV，以及异常处理。
所有示例均围绕生物学场景展开。

运行方式：在终端中执行 python demo.py
"""

import os
import csv

# ============================================================
# 准备工作：确定文件路径
# ============================================================
# os.path.dirname(__file__) 获取当前脚本所在的目录
# 这样无论你从哪个目录运行脚本，文件路径都是正确的
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# 第1部分：写入一个示例 FASTA 文件
# ============================================================
# 我们先用 Python 创建一个 FASTA 文件，模拟从数据库下载序列的场景。
# 这些是简化的示例序列，实际基因序列会长得多。

print("=" * 55)
print("【1】写入示例 FASTA 文件")
print("=" * 55)

# 示例序列数据：3条 DNA 序列
fasta_content = """\
>BRCA1_human 乳腺癌易感基因1
ATGCGTACGTACGATCGATCGTTAAGCGCTAGCTAGC
TAGCATGCGTACGTTAAGCGCATGCGATCGATCGATC
>TP53_human 抑癌基因p53
GGCCAATTGGCCAATTGGCCAATTTGGCCAATTGATC
>EGFR_human 表皮生长因子受体
ATGCGATCGATCGATCGATCGATCGGGCCAATTGGCC
AATTGGCCAATTGATCGATCGATCGATCGATCGATCG
ATCGATCGATCG
"""

# 用 os.path.join 拼接路径，确保跨平台兼容
fasta_path = os.path.join(SCRIPT_DIR, "example_sequences.fasta")

# 使用 with 语句写入文件（"w" 模式 = 写入，会覆盖已有内容）
with open(fasta_path, "w") as f:
    f.write(fasta_content)

print(f"  FASTA 文件已创建: {fasta_path}")
print()


# ============================================================
# 第2部分：读取并解析 FASTA 文件
# ============================================================
# 解析 FASTA 的核心逻辑：
# - 遇到 > 开头的行 → 这是序列名称（标题行）
# - 其他行 → 这是序列内容，拼接到当前序列上

print("=" * 55)
print("【2】解析 FASTA 文件")
print("=" * 55)


def parse_fasta(filepath):
    """
    解析 FASTA 文件，返回字典 {序列名: 序列内容}。

    参数:
        filepath: FASTA 文件的路径

    返回:
        字典，键是序列名称，值是完整的序列字符串
    """
    sequences = {}       # 用字典存储所有序列
    current_name = None  # 当前正在处理的序列名称

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()  # 去掉行首行尾的空白字符和换行符

            if not line:
                # 跳过空行
                continue

            if line.startswith(">"):
                # 标题行：以 > 开头，提取序列名称
                current_name = line[1:]  # 去掉开头的 >
                sequences[current_name] = ""  # 初始化空序列
            else:
                # 序列行：拼接到当前序列
                sequences[current_name] += line

    return sequences


# 调用解析函数
sequences = parse_fasta(fasta_path)

# 打印解析结果
for name, seq in sequences.items():
    print(f"  序列名: {name}")
    print(f"  长度:   {len(seq)} bp")
    # 序列太长时只显示前30个碱基
    display = seq[:30] + "..." if len(seq) > 30 else seq
    print(f"  序列:   {display}")
    print()


# ============================================================
# 第3部分：计算 GC 含量并写入 CSV
# ============================================================
# GC 含量 = (G的个数 + C的个数) / 序列总长度 × 100%

print("=" * 55)
print("【3】计算 GC 含量，保存为 CSV")
print("=" * 55)


def calc_gc(seq):
    """计算 DNA 序列的 GC 含量百分比，保留2位小数。"""
    gc_count = seq.count("G") + seq.count("C")
    return round(gc_count / len(seq) * 100, 2)


# CSV 输出路径
csv_path = os.path.join(SCRIPT_DIR, "gc_results.csv")

# 写入 CSV 文件
# newline="" 参数防止 Windows 上出现多余的空行
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)

    # 写入表头
    writer.writerow(["序列名称", "序列长度(bp)", "GC含量(%)"])

    # 逐条计算并写入
    for name, seq in sequences.items():
        gc = calc_gc(seq)
        writer.writerow([name, len(seq), gc])
        print(f"  {name}: 长度={len(seq)}bp, GC={gc}%")

print(f"\n  结果已保存至: {csv_path}")

# 验证：把刚写入的 CSV 读回来看看
print("\n  --- 验证 CSV 内容 ---")
with open(csv_path, "r") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

print()


# ============================================================
# 第4部分：异常处理 (try/except)
# ============================================================
# 当文件不存在时，程序不应该直接崩溃，而是给出友好的提示。

print("=" * 55)
print("【4】异常处理演示")
print("=" * 55)

# 场景1：尝试读取一个不存在的文件
print("\n  场景1：读取不存在的文件")
fake_path = os.path.join(SCRIPT_DIR, "不存在的文件.fasta")

try:
    with open(fake_path, "r") as f:
        content = f.read()
    print(f"  文件内容: {content}")
except FileNotFoundError:
    print(f"  [捕获异常] 文件不存在: {fake_path}")
    print("  请检查文件路径是否正确！")

# 场景2：数据格式错误
print("\n  场景2：数据格式错误")
bad_values = ["42.5", "hello", "3.14"]

for val in bad_values:
    try:
        number = float(val)
        print(f"  '{val}' → 转换成功: {number}")
    except ValueError:
        print(f"  '{val}' → [捕获异常] 无法转换为数字！")

# 场景3：try/except/finally
print("\n  场景3：finally 块演示")
try:
    result = 10 / 0  # 除以零，一定会报错
except ZeroDivisionError:
    print("  [捕获异常] 不能除以零！")
finally:
    print("  [finally] 无论是否出错，这段代码都会执行。")

print()


# ============================================================
# 清理：删除演示过程中创建的文件（可选）
# ============================================================
# 这里保留文件不删除，方便学生查看生成的 FASTA 和 CSV 文件。
print("=" * 55)
print("演示结束！")
print("=" * 55)
print(f"  生成的文件：")
print(f"    - {fasta_path}")
print(f"    - {csv_path}")
print("  你可以用文本编辑器打开这些文件查看内容。")
