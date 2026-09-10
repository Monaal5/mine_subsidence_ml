"""
Cloud Model — Multi-Output LSTM for Subsidence Forecasting & Severity Estimation
================================================================================
Receives time-series feature vectors from all 5 nodes over a rolling 24-hour window
(288 timesteps) and predicts:
  1. Subsidence Probability (0.0 to 1.0)
  2. Predicted Max Surface Displacement (mm)
  3. Subsidence Severity Class (0: Low, 1: Medium, 2: High)
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import json
import os
import sys

# Ensure reproducible results
SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)

FEATURES = [
    'tilt_mean', 'tilt_rate', 'strain_delta',
    'vib_rms', 'vib_peak', 'vib_dominant_freq',
    'crack_status', 'temp_humidity_index'
]

NODE_IDS = ['N1', 'N2', 'N3', 'N4', 'N5']
NUM_NODES = len(NODE_IDS)
NUM_FEATURES_PER_NODE = len(FEATURES)
TOTAL_INPUT_FEATURES = NUM_NODES * NUM_FEATURES_PER_NODE # 5 * 8 = 40 features per timestep

LOOKBACK_WINDOW = 288  # 24 hours of 5-minute intervals
STEP_SIZE = 12         # Sliding window step (1 hour)


def prepare_sequences():
    """Load dataset, pivot by node, scale features, and create sliding sequences."""
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    feat_path = os.path.join(base_dir, 'dataset', 'feature_vectors_per_node.csv')
    labels_path = os.path.join(base_dir, 'dataset', 'labels.csv')
    
    if not os.path.exists(feat_path):
        print(f"ERROR: Dataset not found at {feat_path}")
        print("Run `python dataset/generate_dataset.py` first.")
        sys.exit(1)
        
    df = pd.read_csv(feat_path)
    
    print(f"Loaded {len(df):,} rows. Pivoting by node...")
    
    # Pivot features so each timestamp has columns for N1..N5
    pivoted_dfs = []
    for node_id in NODE_IDS:
        node_df = df[df['node_id'] == node_id].copy().sort_values('timestamp').reset_index(drop=True)
        node_df = node_df.rename(columns={col: f"{node_id}_{col}" for col in FEATURES})
        pivoted_dfs.append(node_df[['timestamp'] + [f"{node_id}_{col}" for col in FEATURES]])
    
    # Merge all node features on timestamp
    merged = pivoted_dfs[0]
    for n_df in pivoted_dfs[1:]:
        merged = pd.merge(merged, n_df, on='timestamp')
        
    # Merge label (we take the max severity across center nodes N2, N3, N4 as ground truth label)
    df_center = df[df['node_id'].isin(['N2', 'N3', 'N4'])].groupby('timestamp')['label'].max().reset_index()
    merged = pd.merge(merged, df_center, on='timestamp')
    
    feature_cols = [c for c in merged.columns if c not in ['timestamp', 'label']]
    
    # Scale all features
    scaler = StandardScaler()
    scaled_values = scaler.fit_transform(merged[feature_cols].values)
    labels = merged['label'].values
    
    # Create target outputs
    # 1. Probability (1 if pre-subsidence or active, 0 otherwise)
    y_prob = (labels >= 1).astype(np.float32)
    
    # 2. Simulated Displacement mm (0 for normal, 5-30 for pre, 30-150 for active)
    y_disp = np.zeros(len(labels), dtype=np.float32)
    for i in range(len(labels)):
        if labels[i] == 1:
            y_disp[i] = np.random.uniform(5.0, 30.0)
        elif labels[i] == 2:
            y_disp[i] = np.random.uniform(30.0, 150.0)
        elif labels[i] == 3: # Blast
            y_disp[i] = np.random.uniform(0.0, 5.0)
            
    # 3. Severity class (0: Low/Normal, 1: Medium/Pre-subsidence, 2: High/Active)
    y_sev = np.zeros((len(labels), 3), dtype=np.float32)
    for i in range(len(labels)):
        if labels[i] == 0 or labels[i] == 3:
            y_sev[i, 0] = 1.0  # Low
        elif labels[i] == 1:
            y_sev[i, 1] = 1.0  # Medium
        else:
            y_sev[i, 2] = 1.0  # High

    # Create sliding window sequences
    X_seq, y_prob_seq, y_disp_seq, y_sev_seq = [], [], [], []
    
    num_timesteps = len(scaled_values)
    for i in range(0, num_timesteps - LOOKBACK_WINDOW, STEP_SIZE):
        X_seq.append(scaled_values[i:i + LOOKBACK_WINDOW])
        # Target corresponds to the end of the window
        target_idx = i + LOOKBACK_WINDOW
        y_prob_seq.append(y_prob[target_idx])
        y_disp_seq.append(y_disp[target_idx])
        y_sev_seq.append(y_sev[target_idx])
        
    X_seq = np.array(X_seq, dtype=np.float32)
    y_prob_seq = np.array(y_prob_seq, dtype=np.float32)
    y_disp_seq = np.array(y_disp_seq, dtype=np.float32)
    y_sev_seq = np.array(y_sev_seq, dtype=np.float32)
    
    print(f"Generated {len(X_seq):,} sequence windows of shape {X_seq.shape[1:]}")
    
    return X_seq, y_prob_seq, y_disp_seq, y_sev_seq, scaler, feature_cols


def build_cloud_model(input_shape):
    """Build multi-head LSTM network."""
    inputs = keras.Input(shape=input_shape, name="spatial_temporal_input")
    
    x = layers.BatchNormalization()(inputs)
    x = layers.LSTM(64, return_sequences=True)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.LSTM(32, return_sequences=False)(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(32, activation='relu')(x)
    
    # Output Heads
    out_prob = layers.Dense(1, activation='sigmoid', name='subsidence_prob')(x)
    out_disp = layers.Dense(1, activation='linear', name='max_displacement_mm')(x)
    out_sev = layers.Dense(3, activation='softmax', name='severity_class')(x)
    
    model = keras.Model(inputs=inputs, outputs=[out_prob, out_disp, out_sev], name="cloud_subsidence_lstm")
    
    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=0.001),
        loss={
            'subsidence_prob': 'binary_crossentropy',
            'max_displacement_mm': 'huber',
            'severity_class': 'categorical_crossentropy'
        },
        loss_weights={
            'subsidence_prob': 1.0,
            'max_displacement_mm': 0.1,
            'severity_class': 1.0
        },
        metrics={
            'subsidence_prob': ['accuracy', keras.metrics.AUC(name='auc')],
            'severity_class': 'accuracy'
        }
    )
    
    return model


def train():
    print("=" * 70)
    print("Cloud Model Training — Multi-Output LSTM")
    print("=" * 70)
    
    X_seq, y_prob, y_disp, y_sev, scaler, feature_cols = prepare_sequences()
    
    # Train/val split
    indices = np.arange(len(X_seq))
    train_idx, val_idx = train_test_split(indices, test_size=0.2, random_state=SEED, shuffle=True)
    
    X_train, X_val = X_seq[train_idx], X_seq[val_idx]
    
    y_train = {'subsidence_prob': y_prob[train_idx], 'max_displacement_mm': y_disp[train_idx], 'severity_class': y_sev[train_idx]}
    y_val = {'subsidence_prob': y_prob[val_idx], 'max_displacement_mm': y_disp[val_idx], 'severity_class': y_sev[val_idx]}
    
    model = build_cloud_model(input_shape=(LOOKBACK_WINDOW, TOTAL_INPUT_FEATURES))
    model.summary()
    
    callbacks = [
        keras.callbacks.EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=4, verbose=1)
    ]
    
    print("\nStarting Training...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=30,
        batch_size=32,
        callbacks=callbacks,
        verbose=1
    )
    
    # Save artifacts
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    model.save(os.path.join(models_dir, 'cloud_lstm_model.keras'))
    joblib.dump(scaler, os.path.join(models_dir, 'cloud_scaler.pkl'))
    with open(os.path.join(models_dir, 'cloud_feature_cols.json'), 'w') as f:
        json.dump(feature_cols, f, indent=2)
        
    print(f"\nSaved Cloud Model to {models_dir}/cloud_lstm_model.keras")
    print(f"{'=' * 70}")
    print("  Cloud Model Training Complete!")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    train()
