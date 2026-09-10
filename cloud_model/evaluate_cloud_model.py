"""
Cloud Model — Evaluation & Prediction Verification
===================================================
Evaluates the trained LSTM model on unseen sequences, prints accuracy,
MAE for displacement, and saves evaluation plots.
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from sklearn.metrics import classification_report, mean_absolute_error, confusion_matrix
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import sys

from train_cloud_model import prepare_sequences, LOOKBACK_WINDOW, TOTAL_INPUT_FEATURES, SEED

def evaluate_cloud():
    print("=" * 70)
    print("Cloud Model Evaluation — LSTM Multi-Output")
    print("=" * 70)
    
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    models_dir = os.path.join(base_dir, 'models')
    viz_dir = os.path.join(base_dir, 'visualization')
    os.makedirs(viz_dir, exist_ok=True)
    
    model_path = os.path.join(models_dir, 'cloud_lstm_model.keras')
    if not os.path.exists(model_path):
        print(f"ERROR: Model not found at {model_path}")
        sys.exit(1)
        
    model = keras.models.load_model(model_path)
    X_seq, y_prob, y_disp, y_sev, scaler, feature_cols = prepare_sequences()
    
    print("\nRunning model inference on test sequences...")
    pred_prob, pred_disp, pred_sev = model.predict(X_seq, verbose=0)
    
    # 1. Binary Probability Metrics
    pred_binary = (pred_prob.squeeze() > 0.5).astype(int)
    print("\n--- Subsidence Detection Probability ---")
    print(classification_report(y_prob.astype(int), pred_binary, target_names=['Safe/Normal', 'Subsidence Risk'], digits=4))
    
    # 2. Displacement Estimation MAE
    mae = mean_absolute_error(y_disp, pred_disp.squeeze())
    print(f"\n--- Surface Displacement Prediction ---")
    print(f"  Mean Absolute Error (MAE): {mae:.2f} mm")
    
    # 3. Severity Classification Metrics
    y_sev_true_cls = np.argmax(y_sev, axis=1)
    y_sev_pred_cls = np.argmax(pred_sev, axis=1)
    print("\n--- Severity Classification ---")
    print(classification_report(y_sev_true_cls, y_sev_pred_cls, target_names=['Low', 'Medium', 'High'], digits=4))
    
    # Generate Visualization Plots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Cloud Model (LSTM) Evaluation & Forecast Performance', fontsize=16, fontweight='bold')
    
    # Plot 1: Displacement Prediction vs Actual
    ax = axes[0, 0]
    ax.scatter(y_disp, pred_disp.squeeze(), alpha=0.4, color='#3498db', s=15)
    ax.plot([0, 150], [0, 150], 'r--', label='Ideal 1:1 Line')
    ax.set_xlabel('Actual Displacement (mm)')
    ax.set_ylabel('Predicted Displacement (mm)')
    ax.set_title(f'Displacement Estimation (MAE: {mae:.2f} mm)')
    ax.legend()
    
    # Plot 2: Severity Confusion Matrix
    ax = axes[0, 1]
    cm_sev = confusion_matrix(y_sev_true_cls, y_sev_pred_cls)
    sns.heatmap(cm_sev, annot=True, fmt=',d', cmap='Blues', ax=ax,
                xticklabels=['Low', 'Medium', 'High'],
                yticklabels=['Low', 'Medium', 'High'])
    ax.set_xlabel('Predicted Severity')
    ax.set_ylabel('True Severity')
    ax.set_title('Severity Confusion Matrix')
    
    # Plot 3: Probability Trajectory over timeline
    ax = axes[1, 0]
    time_steps = np.arange(len(pred_prob))
    ax.plot(time_steps, pred_prob.squeeze(), color='#e74c3c', label='Predicted Subsidence Risk')
    ax.fill_between(time_steps, 0, pred_prob.squeeze(), color='#e74c3c', alpha=0.2)
    ax.axhline(0.5, color='black', linestyle='--', label='Warning Threshold (0.5)')
    ax.set_xlabel('Sequence Window Index')
    ax.set_ylabel('Risk Probability')
    ax.set_title('Cloud Risk Trajectory Over Time')
    ax.legend()
    
    # Plot 4: Residual Error Distribution for Displacement
    ax = axes[1, 1]
    residuals = y_disp - pred_disp.squeeze()
    sns.histplot(residuals, kde=True, color='#2ecc71', ax=ax)
    ax.set_xlabel('Displacement Residual Error (mm)')
    ax.set_title('Displacement Error Distribution')
    
    plt.tight_layout()
    plot_path = os.path.join(viz_dir, 'cloud_model_evaluation.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"\nSaved evaluation plot to {plot_path}")
    print(f"{'=' * 70}")
    print("  Cloud Model Evaluation Complete!")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    evaluate_cloud()
