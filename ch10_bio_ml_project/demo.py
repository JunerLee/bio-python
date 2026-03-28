"""
第10章 毕业项目：乳腺癌肿瘤诊断分类

完整的机器学习项目流程演示：
    1. 数据加载与探索（EDA）
    2. 特征分析与选择
    3. 数据预处理
    4. 模型训练与调参
    5. 模型评估
    6. 结果可视化与解读

数据集：sklearn 内置 Breast Cancer Wisconsin
目标：区分恶性 (malignant, 0) 和良性 (benign, 1) 肿瘤
"""

# ============================================================
# 环境设置（必须在其他 matplotlib 导入之前）
# ============================================================
import matplotlib

matplotlib.use("Agg")  # 非交互式后端，适合脚本运行和服务器环境

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    RocCurveDisplay,
    accuracy_score,
    classification_report,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# ============================================================
# 全局配置
# ============================================================
# 图片保存目录：与本脚本同一目录
OUTPUT_DIR = Path(__file__).parent
RANDOM_STATE = 42  # 固定随机种子，保证结果可复现

# matplotlib 中文显示设置（尝试常见中文字体，失败则回退）
for font in ["SimHei", "PingFang SC", "WenQuanYi Micro Hei", "DejaVu Sans"]:
    try:
        matplotlib.font_manager.findfont(font, fallback_to_default=False)
        plt.rcParams["font.sans-serif"] = [font]
        break
    except ValueError:
        continue
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题


# ============================================================
# 第1步：数据加载与探索
# ============================================================
def load_data() -> tuple[pd.DataFrame, pd.Series, list[str], list[str]]:
    """加载乳腺癌数据集，返回特征 DataFrame、标签 Series、特征名列表、类别名列表。"""
    data = load_breast_cancer()
    feature_names = list(data.feature_names)
    target_names = list(data.target_names)

    df = pd.DataFrame(data.data, columns=feature_names)
    target = pd.Series(data.target, name="target")

    print("=" * 60)
    print("数据集基本信息")
    print("=" * 60)
    print(f"样本数量: {df.shape[0]}")
    print(f"特征数量: {df.shape[1]}")
    print(f"类别: {target_names}")
    print(f"缺失值总数: {df.isnull().sum().sum()}")
    print(f"\n类别分布:")
    for i, name in enumerate(target_names):
        count = (target == i).sum()
        print(f"  {name} ({i}): {count} 例 ({count / len(target) * 100:.1f}%)")

    return df, target, feature_names, target_names


def explore_data(df: pd.DataFrame) -> None:
    """打印特征的基本统计信息。"""
    print("\n" + "=" * 60)
    print("特征统计摘要（前5个特征）")
    print("=" * 60)
    print(df.iloc[:, :5].describe().round(3).to_string())


# ============================================================
# 第2步：特征分析与选择
# ============================================================
def plot_correlation_heatmap(df: pd.DataFrame, target: pd.Series) -> None:
    """绘制特征相关性热图并保存。"""
    # 将目标变量与特征合并，计算完整相关性矩阵
    full_df = df.copy()
    full_df["target"] = target
    corr_matrix = full_df.corr()

    plt.figure(figsize=(16, 14))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="RdBu_r",
        center=0,
        vmin=-1,
        vmax=1,
        linewidths=0.3,
        fmt=".1f",
    )
    plt.title("Feature Correlation Heatmap", fontsize=16, pad=15)
    plt.tight_layout()

    save_path = OUTPUT_DIR / "correlation_heatmap.png"
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"\n[已保存] 相关性热图 -> {save_path}")


def select_features(
    df: pd.DataFrame, target: pd.Series, top_n: int = 15
) -> list[str]:
    """基于与目标变量的相关性绝对值，选择 top_n 个最重要特征。"""
    correlations = df.corrwith(target).abs().sort_values(ascending=False)

    selected = correlations.head(top_n).index.tolist()

    print(f"\n选择与目标相关性最高的 {top_n} 个特征:")
    for i, feat in enumerate(selected, 1):
        print(f"  {i:2d}. {feat:<30s}  |r| = {correlations[feat]:.4f}")

    return selected


# ============================================================
# 第3步：数据预处理
# ============================================================
def preprocess_data(
    df: pd.DataFrame,
    target: pd.Series,
    selected_features: list[str],
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """数据划分（80/20）+ 标准化。返回 X_train, X_test, y_train, y_test。"""
    X = df[selected_features].values
    y = target.values

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    # 标准化：只在训练集上 fit，防止数据泄漏
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    print(f"\n训练集: {X_train.shape[0]} 例")
    print(f"测试集: {X_test.shape[0]} 例")

    return X_train, X_test, y_train, y_test


# ============================================================
# 第4步：模型训练与交叉验证
# ============================================================
def build_models() -> dict:
    """构建待比较的模型字典。"""
    return {
        "Logistic Regression": LogisticRegression(
            max_iter=2000, random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=100, random_state=RANDOM_STATE
        ),
        "SVM": SVC(kernel="rbf", probability=True, random_state=RANDOM_STATE),
    }


def cross_validate_models(
    models: dict,
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> dict[str, float]:
    """对每个模型进行 5 折交叉验证，返回各模型平均准确率。"""
    print("\n" + "=" * 60)
    print("5 折交叉验证结果")
    print("=" * 60)

    cv_results = {}
    for name, model in models.items():
        scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
        mean_score = scores.mean()
        cv_results[name] = mean_score
        print(f"  {name:<25s}  准确率: {mean_score:.4f} (+/- {scores.std():.4f})")

    return cv_results


# ============================================================
# 第5步：最佳模型评估
# ============================================================
def evaluate_best_model(
    models: dict,
    cv_results: dict[str, float],
    X_train: np.ndarray,
    X_test: np.ndarray,
    y_train: np.ndarray,
    y_test: np.ndarray,
    target_names: list[str],
) -> tuple[str, object]:
    """选出交叉验证最优模型，在测试集上进行完整评估。"""
    best_name = max(cv_results, key=cv_results.get)
    best_model = models[best_name]

    # 在完整训练集上训练
    best_model.fit(X_train, y_train)
    y_pred = best_model.predict(X_test)

    print(f"\n{'=' * 60}")
    print(f"最佳模型: {best_name}")
    print(f"{'=' * 60}")
    print(f"测试集准确率: {accuracy_score(y_test, y_pred):.4f}")
    print(f"\n分类报告:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    # 混淆矩阵
    fig, ax = plt.subplots(figsize=(7, 6))
    ConfusionMatrixDisplay.from_estimator(
        best_model, X_test, y_test, display_labels=target_names, cmap="Blues", ax=ax
    )
    ax.set_title(f"Confusion Matrix ({best_name})", fontsize=14)
    plt.tight_layout()

    save_path = OUTPUT_DIR / "confusion_matrix.png"
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[已保存] 混淆矩阵 -> {save_path}")

    # ROC 曲线
    fig, ax = plt.subplots(figsize=(7, 6))
    RocCurveDisplay.from_estimator(best_model, X_test, y_test, ax=ax)
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Random (AUC=0.5)")
    ax.set_title(f"ROC Curve ({best_name})", fontsize=14)
    ax.legend()
    plt.tight_layout()

    save_path = OUTPUT_DIR / "roc_curve.png"
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[已保存] ROC 曲线 -> {save_path}")

    return best_name, best_model


# ============================================================
# 第6步：特征重要性可视化
# ============================================================
def plot_feature_importance(
    models: dict,
    selected_features: list[str],
    X_train: np.ndarray,
    y_train: np.ndarray,
) -> None:
    """使用 Random Forest 的 feature_importances_ 可视化特征重要性。"""
    rf_model = models["Random Forest"]
    rf_model.fit(X_train, y_train)
    importances = rf_model.feature_importances_

    # 按重要性排序
    indices = np.argsort(importances)[::-1]
    sorted_features = [selected_features[i] for i in indices]
    sorted_importances = importances[indices]

    plt.figure(figsize=(10, 7))
    colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(sorted_features)))
    plt.barh(range(len(sorted_features)), sorted_importances[::-1], color=colors)
    plt.yticks(range(len(sorted_features)), sorted_features[::-1])
    plt.xlabel("Importance", fontsize=12)
    plt.title("Feature Importance (Random Forest)", fontsize=14)
    plt.tight_layout()

    save_path = OUTPUT_DIR / "feature_importance.png"
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[已保存] 特征重要性 -> {save_path}")


# ============================================================
# 主函数：串联完整流程
# ============================================================
def main() -> None:
    """毕业项目完整流程。"""
    print("*" * 60)
    print("  毕业项目：乳腺癌基因表达分类")
    print("*" * 60)

    # 1. 数据加载与探索
    df, target, feature_names, target_names = load_data()
    explore_data(df)

    # 2. 特征分析与选择
    plot_correlation_heatmap(df, target)
    selected_features = select_features(df, target, top_n=15)

    # 3. 数据预处理
    X_train, X_test, y_train, y_test = preprocess_data(df, target, selected_features)

    # 4. 模型训练与交叉验证
    models = build_models()
    cv_results = cross_validate_models(models, X_train, y_train)

    # 5. 最佳模型评估
    best_name, best_model = evaluate_best_model(
        models, cv_results, X_train, X_test, y_train, y_test, target_names
    )

    # 6. 特征重要性可视化
    plot_feature_importance(models, selected_features, X_train, y_train)

    # 最终总结
    print("\n" + "*" * 60)
    print("  项目总结")
    print("*" * 60)
    print(f"  数据集:     Breast Cancer Wisconsin (569 例，形态学特征)")
    print(f"  选用特征:   {len(selected_features)} 个（基于相关性选择）")
    print(f"  最佳模型:   {best_name}")
    print(f"  交叉验证:   {cv_results[best_name]:.4f}")
    print(f"  测试准确率: {accuracy_score(y_test, best_model.predict(X_test)):.4f}")
    print(f"\n  生成图表:")
    print(f"    - correlation_heatmap.png  （特征相关性热图）")
    print(f"    - confusion_matrix.png     （混淆矩阵）")
    print(f"    - roc_curve.png            （ROC 曲线）")
    print(f"    - feature_importance.png   （特征重要性）")
    print("*" * 60)
    print("  恭喜完成毕业项目！")
    print("*" * 60)


if __name__ == "__main__":
    main()
