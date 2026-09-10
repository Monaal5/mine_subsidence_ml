"""
Edge Model — Evaluation & Metrics
==================================
Evaluates the trained Isolation Forest on the full dataset,
generates confusion matrix, ROC curve, and per-class metrics.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, 
    precision_recall_curve, average_precision_score, roc_curve
)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import sys


FEATURES = [
    'tilt_mean', 'tilt_rate', 'strain_delta',
    'vib_rms', 'vib_peak', 'vib_dominant_freq',
    'crack_status', 'temp_humidity_index'
]

LABEL_NAMES = {0: 'Normal', 1: 'Pre-Subsidence', 2: 'Active Subsidence', 3: 'Blast'}


def load_assets():
    """Load model, scaler, threshold, and dataset."""
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    models_dir = os.path.join(base_dir, 'models')
    data_dir = os.path.join(base_dir, 'dataset')
    
    model = joblib.load(os.path.join(models_dir, 'isolation_forest.pkl'))
    scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
    threshold = np.load(os.path.join(models_dir, 'anomaly_threshold.npy'))
    df = pd.read_csv(os.path.join(data_dir, 'feature_vectors_per_node.csv'))
    
    return model, scaler, float(threshold), df


def evaluate(model, scaler, threshold, df):
    """Run evaluation on the full dataset."""
    
    print("=" * 70)
    print("Edge Model Evaluation — Isolation Forest")
    print("=" * 70)
    
    X = df[FEATURES].values
    y_true_multi = df['label'].values
    
    # Binary labels: 0=normal, 1=anomaly (any non-normal)
    y_true_binary = (y_true_multi > 0).astype(int)
    
    # Scale features
    X_scaled = scaler.transform(X)
    
    # Get anomaly scores
    scores = model.score_samples(X_scaled)
    
    # Predict using threshold
    y_pred_binary = (scores < threshold).astype(int)
    
    # === METRICS ===
    print(f"\nThreshold: {threshold:.5f}")
    print(f"\n--- Binary Classification (Normal vs Anomaly) ---")
    print(classification_report(
        y_true_binary, y_pred_binary, 
        target_names=['Normal', 'Anomaly'],
        digits=4
    ))
    
    # Confusion Matrix
    cm = confusion_matrix(y_true_binary, y_pred_binary)
    print(f"Confusion Matrix:")
    print(f"  TN={cm[0,0]:,}  FP={cm[0,1]:,}")
    print(f"  FN={cm[1,0]:,}  TP={cm[1,1]:,}")
    
    # False Positive Rate
    fpr = cm[0,1] / (cm[0,0] + cm[0,1]) if (cm[0,0] + cm[0,1]) > 0 else 0
    fnr = cm[1,0] / (cm[1,0] + cm[1,1]) if (cm[1,0] + cm[1,1]) > 0 else 0
    print(f"\n  False Positive Rate: {fpr:.4f} ({fpr*100:.2f}%)")
    print(f"  False Negative Rate: {fnr:.4f} ({fnr*100:.2f}%)")
    
    # AUC-ROC
    auc = roc_auc_score(y_true_binary, -scores)  # negate: lower score = more anomalous
    print(f"  AUC-ROC: {auc:.4f}")
    
    # Average Precision
    ap = average_precision_score(y_true_binary, -scores)
    print(f"  Average Precision: {ap:.4f}")
    
    # === PER-CLASS ANALYSIS ===
    print(f"\n--- Per-Class Detection Rates ---")
    for label, name in LABEL_NAMES.items():
        mask = y_true_multi == label
        if mask.sum() == 0:
            continue
        class_scores = scores[mask]
        detected = (class_scores < threshold).sum()
        total = mask.sum()
        rate = detected / total
        print(f"  {name:20s}: {detected:6,}/{total:6,} detected ({rate*100:.1f}%)")
    
    # === PER-NODE ANALYSIS ===
    print(f"\n--- Per-Node Detection Rates ---")
    for node_id in df['node_id'].unique():
        node_mask = df['node_id'] == node_id
        node_anomaly_mask = node_mask & (y_true_multi > 0)
        if node_anomaly_mask.sum() == 0:
            continue
        node_scores = scores[node_anomaly_mask]
        detected = (node_scores < threshold).sum()
        total = node_anomaly_mask.sum()
        rate = detected / total
        print(f"  {node_id}: {detected:,}/{total:,} anomalies detected ({rate*100:.1f}%)")
    
    return scores, y_true_binary, y_pred_binary


def plot_results(scores, y_true_binary, df, threshold):
    """Generate evaluation plots."""
    
    viz_dir = os.path.join(os.path.dirname(__file__), '..', 'visualization')
    os.makedirs(viz_dir, exist_ok=True)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Edge Model (Isolation Forest) — Evaluation', fontsize=16, fontweight='bold')
    
    # 1. Score Distribution
    ax = axes[0, 0]
    normal_scores = scores[y_true_binary == 0]
    anomaly_scores = scores[y_true_binary == 1]
    ax.hist(normal_scores, bins=100, alpha=0.7, label='Normal', color='#2ecc71', density=True)
    ax.hist(anomaly_scores, bins=100, alpha=0.7, label='Anomaly', color='#e74c3c', density=True)
    ax.axvline(threshold, color='#f39c12', linestyle='--', linewidth=2, label=f'Threshold ({threshold:.3f})')
    ax.set_xlabel('Anomaly Score')
    ax.set_ylabel('Density')
    ax.set_title('Score Distribution')
    ax.legend()
    
    # 2. ROC Curve
    ax = axes[0, 1]
    fpr_curve, tpr_curve, _ = roc_curve(y_true_binary, -scores)
    auc_val = roc_auc_score(y_true_binary, -scores)
    ax.plot(fpr_curve, tpr_curve, color='#3498db', linewidth=2, label=f'AUC = {auc_val:.4f}')
    ax.plot([0, 1], [0, 1], 'k--', alpha=0.3)
    ax.set_xlabel('False Positive Rate')
    ax.set_ylabel('True Positive Rate')
    ax.set_title('ROC Curve')
    ax.legend()
    
    # 3. Scores over Time (Node N3 — center)
    ax = axes[1, 0]
    n3_mask = df['node_id'] == 'N3'
    n3_scores = scores[n3_mask]
    n3_labels = df[n3_mask]['label'].values
    days = np.arange(len(n3_scores)) / 288  # 288 samples per day
    
    colors = {0: '#2ecc71', 1: '#f39c12', 2: '#e74c3c', 3: '#9b59b6'}
    for label, color in colors.items():
        mask = n3_labels == label
        ax.scatter(days[mask], n3_scores[mask], s=1, c=color, alpha=0.3,
                   label=LABEL_NAMES[label])
    ax.axhline(threshold, color='#e74c3c', linestyle='--', linewidth=1.5, alpha=0.8)
    ax.set_xlabel('Day')
    ax.set_ylabel('Anomaly Score')
    ax.set_title('Anomaly Scores Over Time (Node N3 — Center)')
    ax.legend(markerscale=5, loc='lower left')
    
    # 4. Confusion Matrix Heatmap
    ax = axes[1, 1]
    y_pred = (scores < threshold).astype(int)
    cm = confusion_matrix(y_true_binary, y_pred)
    sns.heatmap(cm, annot=True, fmt=',d', cmap='Blues', ax=ax,
                xticklabels=['Normal', 'Anomaly'],
                yticklabels=['Normal', 'Anomaly'])
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title('Confusion Matrix')
    
    plt.tight_layout()
    
    plot_path = os.path.join(viz_dir, 'edge_model_evaluation.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n  Evaluation plot saved: {plot_path}")


def main():
    model, scaler, threshold, df = load_assets()
    scores, y_true, y_pred = evaluate(model, scaler, threshold, df)
    plot_results(scores, y_true, df, threshold)
    print(f"\n{'=' * 70}")
    print("  Edge Model Evaluation Complete!")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    main()
