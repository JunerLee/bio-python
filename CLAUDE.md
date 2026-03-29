# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目简介

面向零基础生物学本科生的 10 章 Python 教程。所有概念用生物学类比讲解（变量=试管，函数=酶，循环=PCR），从 `print()` 逐步推进到乳腺癌分类机器学习项目。

**全教程内容（讲义、注释、文档字符串、print 输出）使用简体中文**，代码标识符使用英文。

## 常用命令

```bash
uv sync                        # 安装依赖（使用清华 PyPI 镜像）
uv run python chXX_章节名/demo.py       # 运行章节演示
uv run python chXX_章节名/solutions.py  # 运行参考答案
uv run python chXX_章节名/exercises.py  # 运行学生练习（含 TODO 占位）
```

无测试框架、无 linter 配置、无 CI/CD。验证代码正确性的唯一方式是 `uv run python` 运行脚本并检查输出。

## 章节结构

每章目录遵循统一布局：

```
chXX_章节名/
├── lecture.md      # 讲义（中文讲解 + mermaid/SVG 配图）
├── demo.py         # 可运行的演示代码
├── exercises.py    # 学生版练习（# TODO: 占位 + pass）
├── solutions.py    # 教师版完整答案
└── assets/         # SVG 插图
```

章节难度递进：
- Ch1-4：Python 基础（print、数据类型、控制流、函数）
- Ch5：文件读写（FASTA 解析、CSV、异常处理）
- Ch6-7：数据科学（NumPy 数组、Pandas DataFrame）
- Ch8：可视化（matplotlib、seaborn、热图、火山图）
- Ch9-10：机器学习（KNN、决策树、随机森林、SVM、PCA）

## 代码风格约定

- 代码段落用 `# ============================================================` 分隔
- 大量使用 f-string 格式化输出
- 每段代码前有中文注释解释生物学动机
- matplotlib 使用 `Agg` 后端（无头模式），中文字体通过 `plt.rcParams['font.sans-serif']` 配置
- 输出路径模式：`OUTPUT_DIR = Path(__file__).parent`
- ML 章节固定随机种子：`RANDOM_STATE = 42`
- 后期章节（ch9、ch10）使用 `if __name__ == "__main__":` 守卫和类型注解
- exercises.py 中未完成的 TODO 会打印引导信息，而非静默失败

## 机器学习章节注意点

ch9 和 ch10 是数据泄漏防护的教学重点：
- 先 train/test 分割再做特征选择
- 使用 Pipeline 防止 scaler 在交叉验证中泄漏
- 这一点在 commit `8d7eccb` 中专门修复过，修改时务必保持

## 生成文件（已在 .gitignore 中）

运行 demo/solutions 会产生的本地文件：PNG 图片（ch8/9/10）、CSV（ch5/7）、FASTA（ch5）、文本报告（ch5）。不要提交这些文件。
