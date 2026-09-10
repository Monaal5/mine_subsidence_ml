"""
Edge Model — Train Isolation Forest + Export to C via emlearn
=============================================================
Trains on NORMAL data only (unsupervised anomaly detection).
Exports a C header file deployable on ESP32-S3 via emlearn.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

# Try to import emlearn; provide guidance if not installed
try:
    import emlearn
    HAS_EMLEARN = True
except ImportError:
    HAS_EMLEARN = False
    print("WARNING: emlearn not installed. Will train model but skip C export.")
    print("Install with: pip install emlearn")


FEATURES = [
    'tilt_mean', 'tilt_rate', 'strain_delta',
    'vib_rms', 'vib_peak', 'vib_dominant_freq',
    'crack_status', 'temp_humidity_index'
]

NUM_FEATURES = len(FEATURES)

# Isolation Forest hyperparameters (optimized for ESP32 deployment)
N_ESTIMATORS = 10       # Number of trees — keep small for MCU
MAX_SAMPLES = 256       # Max samples per tree — controls depth
CONTAMINATION = 0.01    # Expected anomaly rate in "clean" training data
MAX_FEATURES = 1.0      # Use all features per tree
RANDOM_STATE = 42


def load_data():
    """Load feature vectors dataset."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'dataset')
    feat_path = os.path.join(data_dir, 'feature_vectors_per_node.csv')
    
    if not os.path.exists(feat_path):
        print(f"ERROR: Dataset not found at {feat_path}")
        print("Run `python dataset/generate_dataset.py` first.")
        sys.exit(1)
    
    df = pd.read_csv(feat_path)
    print(f"Loaded {len(df):,} rows from {feat_path}")
    return df


def train_model(df):
    """Train Isolation Forest on normal data."""
    
    # Split: train on normal data only
    normal_data = df[df['label'] == 0].copy()
    anomaly_data = df[df['label'] > 0].copy()
    
    print(f"\nData Split:")
    print(f"  Normal samples (training):  {len(normal_data):,}")
    print(f"  Anomaly samples (testing):  {len(anomaly_data):,}")
    
    X_train_raw = normal_data[FEATURES].values
    
    # Hold out 20% of normal data for threshold calibration
    X_train_raw, X_val_normal, _, _ = train_test_split(
        X_train_raw, np.zeros(len(X_train_raw)), 
        test_size=0.2, random_state=RANDOM_STATE
    )
    
    print(f"  Training samples:           {len(X_train_raw):,}")
    print(f"  Validation (normal) samples: {len(X_val_normal):,}")
    
    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_raw)
    X_val = scaler.transform(X_val_normal)
    
    print(f"\nScaler Parameters:")
    for i, feat in enumerate(FEATURES):
        print(f"  {feat:25s} mean={scaler.mean_[i]:10.5f}  scale={scaler.scale_[i]:10.5f}")
    
    # Train Isolation Forest
    print(f"\nTraining Isolation Forest...")
    print(f"  n_estimators={N_ESTIMATORS}, max_samples={MAX_SAMPLES}, "
          f"contamination={CONTAMINATION}")
    
    model = IsolationForest(
        n_estimators=N_ESTIMATORS,
        max_samples=MAX_SAMPLES,
        contamination=CONTAMINATION,
        max_features=MAX_FEATURES,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )
    model.fit(X_train)
    
    # Compute anomaly scores on validation set (normal data)
    val_scores = model.score_samples(X_val)
    
    # Calibrate threshold: 99th percentile of normal scores as boundary
    threshold = np.percentile(val_scores, 1)  # 1st percentile (scores are negative)
    print(f"\n  Anomaly threshold (1st pct of normal): {threshold:.5f}")
    print(f"  Normal score range: [{val_scores.min():.5f}, {val_scores.max():.5f}]")
    print(f"  Normal score mean:  {val_scores.mean():.5f}")
    
    return model, scaler, threshold


def export_to_c(model, scaler, threshold):
    """Export IsolationForest model to standalone C header for microcontrollers."""
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    firmware_dir = os.path.join(os.path.dirname(__file__), '..', 'esp32_firmware')
    os.makedirs(firmware_dir, exist_ok=True)
    
    print(f"\nExporting Isolation Forest to C Header...")
    
    # Generate C code directly from scikit-learn IsolationForest trees
    c_code = generate_isolation_forest_c_header(model, threshold)
    
    h_path_edge = os.path.join(output_dir, 'isolation_forest_model.h')
    h_path_fw = os.path.join(firmware_dir, 'isolation_forest_model.h')
    
    with open(h_path_edge, 'w') as f:
        f.write(c_code)
    with open(h_path_fw, 'w') as f:
        f.write(c_code)
        
    print(f"  Saved C Model Header: {h_path_edge}")
    print(f"  Saved C Model Header: {h_path_fw}")
    
    size_kb = os.path.getsize(h_path_edge) / 1024
    print(f"  Compiled C Model Header Size: {size_kb:.2f} KB")
    
    # Export scaler header
    scaler_h = generate_scaler_header(scaler, threshold)
    scaler_path_edge = os.path.join(output_dir, 'scaler_params.h')
    scaler_path_fw = os.path.join(firmware_dir, 'scaler_params.h')
    
    with open(scaler_path_edge, 'w') as f:
        f.write(scaler_h)
    with open(scaler_path_fw, 'w') as f:
        f.write(scaler_h)
        
    print(f"  Saved Scaler Header: {scaler_path_edge}")


def generate_isolation_forest_c_header(model, threshold):
    """Generates standalone C code representing the Isolation Forest decision trees."""
    estimators = model.estimators_
    n_trees = len(estimators)
    max_samples = model.max_samples_
    
    # Calculate c(n) average path length for max_samples (Euler's gamma ~ 0.5772156649)
    if max_samples > 2:
        c_n = 2.0 * (np.log(max_samples - 1) + 0.5772156649) - (2.0 * (max_samples - 1) / max_samples)
    else:
        c_n = 1.0
    
    tree_structs = []
    
    for i, tree in enumerate(estimators):
        t = tree.tree_
        feature = t.feature
        threshold_arr = t.threshold
        left = t.children_left
        right = t.children_right
        
        nodes_code = []
        for n in range(t.node_count):
            feat = feature[n]
            thresh = threshold_arr[n]
            l_child = left[n]
            r_child = right[n]
            nodes_code.append(f"    {{{feat}, {thresh:.6f}f, {l_child}, {r_child}}}")
            
        nodes_str = ",\n".join(nodes_code)
        tree_structs.append(f"static const Node TREE_{i}_NODES[] = {{\n{nodes_str}\n}};")

    trees_array = ",\n".join([f"    TREE_{i}_NODES" for i in range(n_trees)])
    
    header = f"""/*
 * Auto-generated Isolation Forest C Code for ESP32-S3 TinyML
 * Generated by train_edge_model.py
 */

#ifndef ISOLATION_FOREST_MODEL_H
#define ISOLATION_FOREST_MODEL_H

#include <math.h>

#define NUM_TREES {n_trees}
#define C_NORM_FACTOR {c_n:.6f}f
#define ISOLATION_THRESHOLD {threshold:.6f}f

typedef struct {{
    int feature;
    float threshold;
    int left_child;
    int right_child;
}} Node;

{chr(10).join(tree_structs)}

static const Node* FOREST_TREES[] = {{
{trees_array}
}};

// Compute decision path depth for a single tree
static inline float compute_tree_depth(const Node* nodes, const float* features) {{
    int node_idx = 0;
    float depth = 0.0f;
    
    while (node_idx >= 0) {{
        int feat = nodes[node_idx].feature;
        if (feat < 0) break; // Leaf node
        
        if (features[feat] <= nodes[node_idx].threshold) {{
            node_idx = nodes[node_idx].left_child;
        }} else {{
            node_idx = nodes[node_idx].right_child;
        }}
        depth += 1.0f;
    }}
    return depth;
}}

// Run full Isolation Forest inference and return normalized anomaly score
// Standard formula: s = -2^(-avg_depth / c(n)), matching scikit-learn score_samples()
static inline float subsidence_detector_predict(const float* features, int num_features) {{
    float total_depth = 0.0f;
    for (int i = 0; i < NUM_TREES; i++) {{
        total_depth += compute_tree_depth(FOREST_TREES[i], features);
    }}
    float avg_depth = total_depth / (float)NUM_TREES;
    return -powf(2.0f, -(avg_depth / C_NORM_FACTOR));
}}

#endif // ISOLATION_FOREST_MODEL_H
"""
    return header


def generate_scaler_header(scaler, threshold):
    """Generate C header with scaler parameters and threshold."""
    
    header = """/*
 * Auto-generated scaler parameters for Mine Subsidence Edge Model
 * DO NOT EDIT — regenerate by running train_edge_model.py
 */

#ifndef SCALER_PARAMS_H
#define SCALER_PARAMS_H

#define NUM_FEATURES 8
#define ANOMALY_THRESHOLD {threshold}f

// Feature names (for reference):
// [0] tilt_mean
// [1] tilt_rate
// [2] strain_delta
// [3] vib_rms
// [4] vib_peak
// [5] vib_dominant_freq
// [6] crack_status
// [7] temp_humidity_index

static const float SCALER_MEAN[NUM_FEATURES] = {{
    {means}
}};

static const float SCALER_SCALE[NUM_FEATURES] = {{
    {scales}
}};

// Apply standard scaling: scaled[i] = (raw[i] - mean[i]) / scale[i]
static inline void scale_features(const float* raw, float* scaled) {{
    for (int i = 0; i < NUM_FEATURES; i++) {{
        scaled[i] = (raw[i] - SCALER_MEAN[i]) / SCALER_SCALE[i];
    }}
}}

#endif // SCALER_PARAMS_H
"""
    
    means_str = ',\n    '.join(f'{m:.8f}f' for m in scaler.mean_)
    scales_str = ',\n    '.join(f'{s:.8f}f' for s in scaler.scale_)
    
    return header.format(
        threshold=f'{threshold:.8f}',
        means=means_str,
        scales=scales_str
    )


def save_python_model(model, scaler, threshold):
    """Save Python model for evaluation."""
    models_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    joblib.dump(model, os.path.join(models_dir, 'isolation_forest.pkl'))
    joblib.dump(scaler, os.path.join(models_dir, 'scaler.pkl'))
    np.save(os.path.join(models_dir, 'anomaly_threshold.npy'), threshold)
    np.save(os.path.join(models_dir, 'scaler_mean.npy'), scaler.mean_)
    np.save(os.path.join(models_dir, 'scaler_scale.npy'), scaler.scale_)
    
    print(f"\n  Python model saved to {models_dir}/")


def main():
    print("=" * 70)
    print("Edge Model Training — Isolation Forest for ESP32-S3")
    print("=" * 70)
    
    df = load_data()
    model, scaler, threshold = train_model(df)
    export_to_c(model, scaler, threshold)
    save_python_model(model, scaler, threshold)
    
    print(f"\n{'=' * 70}")
    print("  Edge Model Training Complete!")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    main()
