import os
import pickle

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ===== المسارات =====
DATA_PATH = os.environ.get("DATA_PATH", "DARWIN.csv")
ARTIFACTS_DIR = "artifacts"
MODEL_PATH = os.path.join(ARTIFACTS_DIR, "model_artifacts.pkl")

# ===== عدد الـ Features المراد اختيارها تلقائياً =====
TOP_N_FEATURES = 20


def load_data():
    """تحميل البيانات من CSV وتجهيز X و y"""
    print(f"📂 Loading data from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)

    if "class" not in df.columns:
        raise ValueError("Column 'class' not found in DARWIN.csv")

    df = df.dropna(subset=["class"])

    # تحويل H -> 0, P -> 1
    y = df["class"].map({"H": 0, "P": 1})
    if y.isnull().any():
        raise ValueError("Found values other than H/P in 'class' column")

    # حذف الأعمدة غير المطلوبة
    drop_cols = [c for c in ["ID", "class"] if c in df.columns]
    X = df.drop(columns=drop_cols)

    # التعامل مع القيم الناقصة
    X = X.fillna(X.mean())

    print(f"✅ Data loaded: {X.shape[0]} samples, {X.shape[1]} features")
    return X, y


def select_top_features(X_train, y_train, n_features=TOP_N_FEATURES):
    """اختيار أفضل N feature بناءً على Feature Importance من Random Forest"""
    print(f"\n🔍 Selecting top {n_features} features from {X_train.shape[1]} total features...")

    # تدريب نموذج مبدئي لحساب أهمية الـ features
    selector_model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1,
    )
    selector_model.fit(X_train, y_train)

    # ترتيب الـ features حسب الأهمية
    importances = pd.Series(
        selector_model.feature_importances_,
        index=X_train.columns
    ).sort_values(ascending=False)

    # اختيار أفضل N feature
    top_features = importances.head(n_features).index.tolist()

    print(f"\n🏆 Top {n_features} Selected Features:")
    for i, (feat, imp) in enumerate(importances.head(n_features).items(), 1):
        print(f"  {i:2d}. {feat:<40} importance: {imp:.4f}")

    return top_features, importances


def compute_feature_stats(X_sel):
    """حساب إحصائيات كل feature للاستخدام في الـ sliders"""
    stats = {}
    for col in X_sel.columns:
        col_data = X_sel[col].astype(float)
        col_min = float(col_data.min())
        col_max = float(col_data.max())
        col_mean = float(col_data.mean())

        if col_min == col_max:
            col_min -= 1.0
            col_max += 1.0

        stats[col] = {
            "min": col_min,
            "max": col_max,
            "mean": col_mean,
            "step": (col_max - col_min) / 100.0 if col_max > col_min else 0.01,
        }
    return stats


def train_and_save():
    # 1. تحميل البيانات
    X, y = load_data()

    # 2. تقسيم البيانات
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 3. اختيار أفضل الـ features تلقائياً
    top_features, all_importances = select_top_features(X_train, y_train, TOP_N_FEATURES)

    # 4. تصفية البيانات على الـ features المختارة فقط
    X_train_sel = X_train[top_features]
    X_test_sel = X_test[top_features]

    # 5. بناء الـ Pipeline النهائي
    print(f"\n🚀 Training final model on top {TOP_N_FEATURES} features...")
    pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("model", RandomForestClassifier(
            n_estimators=400,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )),
    ])

    pipe.fit(X_train_sel, y_train)

    # 6. تقييم النموذج
    print("\n==== Evaluation on hold-out test set ====")
    y_pred = pipe.predict(X_test_sel)
    print(classification_report(y_test, y_pred, target_names=["Healthy", "Patient"]))

    # 7. Cross-validation
    print("==== 5-Fold Cross-Validation ====")
    cv_scores = cross_val_score(pipe, X_train_sel, y_train, cv=5, scoring="f1_macro")
    print(f"F1 Macro: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")

    # 8. حساب إحصائيات الـ features
    feature_stats = compute_feature_stats(X[top_features])
    label_map = {0: "Healthy", 1: "Patient"}

    # 9. حفظ كل شيء
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    artifacts = {
        "pipeline": pipe,
        "feature_names": top_features,
        "feature_stats": feature_stats,
        "label_map": label_map,
        "feature_importances": all_importances.to_dict(),
    }

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(artifacts, f)

    print(f"\n✅ Saved model artifacts to {MODEL_PATH}")
    print(f"✅ Selected features: {top_features}")


if __name__ == "__main__":
    train_and_save()