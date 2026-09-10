"""
Mine Subsidence Monitoring — Physics-Informed Synthetic Dataset Generator
=========================================================================
Generates realistic sensor data for 5 surface-mounted nodes over 90 days,
simulating Normal → Pre-Subsidence → Active Subsidence phases with blast
event injections. Based on Indian longwall mining reference parameters.

Output:
  - raw_sensor_data.csv          (all nodes, all timestamps, all raw sensors)
  - feature_vectors_per_node.csv (extracted features per 5-min window)
  - labels.csv                   (0=normal, 1=pre-subsidence, 2=active, 3=blast)
  - node_positions.csv           (node_id, x_m, y_m)
  - metadata.json                (generation parameters)
"""

import numpy as np
import pandas as pd
import json
import os
from datetime import datetime, timedelta
from scipy.signal import butter, filtfilt

# ============================================================================
# CONFIGURATION
# ============================================================================
SEED = 42
np.random.seed(SEED)

# Panel & Node Layout
PANEL_WIDTH_M = 200       # meters
PANEL_LENGTH_M = 1500     # meters
NUM_NODES = 5

# Node positions (grid on panel surface)
# Nodes arranged: 2 edge, 1 center, 2 mid-zone
NODE_POSITIONS = {
    'N1': {'x': 30,  'y': 375,  'zone': 'edge'},       # Edge node (west)
    'N2': {'x': 80,  'y': 750,  'zone': 'mid'},         # Mid-zone
    'N3': {'x': 100, 'y': 750,  'zone': 'center'},      # Center (max subsidence)
    'N4': {'x': 130, 'y': 750,  'zone': 'mid'},         # Mid-zone
    'N5': {'x': 170, 'y': 1125, 'zone': 'edge'},        # Edge node (east)
}

# Simulation timeline
TOTAL_DAYS = 90
SAMPLE_INTERVAL_MIN = 5
SAMPLES_PER_DAY = 24 * 60 // SAMPLE_INTERVAL_MIN  # 288
TOTAL_SAMPLES = TOTAL_DAYS * SAMPLES_PER_DAY       # 25920

# Phase boundaries (day indices)
NORMAL_END = 60
PRE_SUBSIDENCE_END = 75
ACTIVE_END = 85
# Days 85-90: partial recovery / stabilization

# Blast events: (day, hour, duration_samples)
BLAST_EVENTS = [
    (12, 14, 3),   # Day 12, 2 PM, 15 min
    (28, 10, 2),   # Day 28, 10 AM, 10 min
    (45, 16, 4),   # Day 45, 4 PM, 20 min
    (68, 11, 3),   # Day 68, 11 AM, 15 min (during pre-subsidence!)
    (82, 9, 2),    # Day 82, 9 AM, 10 min (during active subsidence!)
]

# Subsidence spatial influence — distance from panel center
# Nodes closer to center are affected first and most severely
def subsidence_influence(node_pos, panel_center_x=100, panel_center_y=750):
    """Returns a factor 0-1 indicating how strongly this node is affected.
    Center node gets ~1.0, edge nodes get ~0.2-0.4."""
    dx = abs(node_pos['x'] - panel_center_x) / (PANEL_WIDTH_M / 2)
    dy = abs(node_pos['y'] - panel_center_y) / (PANEL_LENGTH_M / 2)
    dist_norm = np.sqrt(dx**2 + dy**2)
    # Gaussian-like influence
    influence = np.exp(-2.0 * dist_norm**2)
    return np.clip(influence, 0.15, 1.0)

def subsidence_onset_delay_days(influence):
    """Nodes further from center get hit later. Max delay = 5 days."""
    return int((1.0 - influence) * 5)

# ============================================================================
# SIGNAL GENERATORS
# ============================================================================

def diurnal_cycle(sample_indices, amplitude, offset, phase_shift=0):
    """Sinusoidal diurnal pattern (24-hour period)."""
    period = SAMPLES_PER_DAY
    return offset + amplitude * np.sin(2 * np.pi * sample_indices / period + phase_shift)

def seasonal_drift(sample_indices, total_samples, amplitude):
    """Slow seasonal drift over the full simulation."""
    return amplitude * np.sin(2 * np.pi * sample_indices / total_samples)

def sigmoid_ramp(x, center, steepness):
    """Sigmoid transition for gradual subsidence onset."""
    return 1.0 / (1.0 + np.exp(-steepness * (x - center)))

def generate_subsidence_tilt_profile(num_samples, onset_sample, peak_sample, 
                                      max_tilt_deg, influence_factor):
    """Generate realistic tilt progression: flat → sigmoid ramp → accelerating."""
    tilt = np.zeros(num_samples)
    max_tilt = max_tilt_deg * influence_factor
    
    for i in range(num_samples):
        if i < onset_sample:
            tilt[i] = 0.0
        elif i < peak_sample:
            progress = (i - onset_sample) / (peak_sample - onset_sample)
            # Sigmoid-shaped onset, then accelerating
            tilt[i] = max_tilt * (sigmoid_ramp(progress, 0.3, 10) * 0.3 + 
                                   progress**2 * 0.7)
        else:
            # Post-peak: slight stabilization with continued high tilt
            decay = 0.95 + 0.05 * np.exp(-0.01 * (i - peak_sample))
            tilt[i] = max_tilt * decay
    
    return tilt

def generate_strain_profile(num_samples, onset_sample, peak_sample,
                             max_strain_ue, influence_factor):
    """Strain increases with subsidence, with step jumps simulating crack propagation."""
    strain = np.zeros(num_samples)
    max_s = max_strain_ue * influence_factor
    
    for i in range(num_samples):
        if i < onset_sample:
            strain[i] = 0.0
        elif i < peak_sample:
            progress = (i - onset_sample) / (peak_sample - onset_sample)
            base = max_s * progress**1.5
            # Random step jumps (crack propagation events)
            if np.random.random() < 0.001 * progress:
                base += np.random.uniform(2, 8)
            strain[i] = base
        else:
            strain[i] = max_s * (0.9 + 0.1 * np.random.random())
    
    return strain

# ============================================================================
# MAIN DATASET GENERATOR
# ============================================================================

def generate_node_data(node_id, node_pos, influence):
    """Generate all sensor channels for a single node."""
    
    n = TOTAL_SAMPLES
    indices = np.arange(n)
    onset_delay = subsidence_onset_delay_days(influence)
    
    # Phase sample boundaries (adjusted for this node's delay)
    normal_end_s = NORMAL_END * SAMPLES_PER_DAY
    pre_sub_start_s = (NORMAL_END + onset_delay) * SAMPLES_PER_DAY
    pre_sub_end_s = PRE_SUBSIDENCE_END * SAMPLES_PER_DAY
    active_end_s = ACTIVE_END * SAMPLES_PER_DAY
    
    # === TILT X & Y ===
    # Normal: noise + thermal diurnal drift
    tilt_noise_x = np.random.normal(0, 0.015, n)
    tilt_noise_y = np.random.normal(0, 0.012, n)
    tilt_diurnal_x = diurnal_cycle(indices, 0.02, 0, phase_shift=0.5)
    tilt_diurnal_y = diurnal_cycle(indices, 0.015, 0, phase_shift=0.8)
    
    # Subsidence tilt ramp
    tilt_sub_x = generate_subsidence_tilt_profile(
        n, pre_sub_start_s, active_end_s, max_tilt_deg=1.8, influence_factor=influence
    )
    tilt_sub_y = generate_subsidence_tilt_profile(
        n, pre_sub_start_s, active_end_s, max_tilt_deg=1.2, influence_factor=influence
    )
    
    tilt_x = tilt_noise_x + tilt_diurnal_x + tilt_sub_x
    tilt_y = tilt_noise_y + tilt_diurnal_y + tilt_sub_y
    
    # === STRAIN ===
    strain_noise = np.random.normal(0, 0.8, n)
    strain_diurnal = diurnal_cycle(indices, 0.5, 0, phase_shift=1.2)
    strain_sub = generate_strain_profile(
        n, pre_sub_start_s, active_end_s, max_strain_ue=45, influence_factor=influence
    )
    strain_delta = strain_noise + strain_diurnal + strain_sub
    
    # === VIBRATION ===
    # Normal: low-amplitude ambient
    vib_rms = np.abs(np.random.normal(0.025, 0.01, n))
    vib_peak = vib_rms * np.random.uniform(1.5, 3.0, n)
    vib_freq = np.random.uniform(8, 18, n)  # ambient: 8-18 Hz
    
    # Subsidence: increased low-freq vibration
    for i in range(n):
        if i >= pre_sub_start_s:
            progress = min(1.0, (i - pre_sub_start_s) / (active_end_s - pre_sub_start_s))
            vib_rms[i] += 0.08 * progress * influence
            vib_peak[i] += 0.25 * progress * influence
            # Frequency shifts lower during subsidence (strata failure = low freq)
            vib_freq[i] = max(2.0, vib_freq[i] - 12 * progress * influence)
    
    # === CRACK SENSOR ===
    crack = np.ones(n, dtype=int)  # 1 = intact
    if influence > 0.5:
        # Crack breaks during active subsidence for high-influence nodes
        crack_break_sample = int(active_end_s - 
                                  (active_end_s - pre_sub_end_s) * (influence - 0.5))
        crack[crack_break_sample:] = 0
    elif influence > 0.3:
        # Edge nodes: crack may break late in active phase
        crack_break_sample = int(active_end_s - SAMPLES_PER_DAY * 2)
        crack[crack_break_sample:] = 0
    
    # === ENVIRONMENTAL (BME280) ===
    # Temperature: 25-42°C diurnal, seasonal variation
    temp = diurnal_cycle(indices, 8.0, 33.0, phase_shift=0.3)
    temp += seasonal_drift(indices, n, 3.0)
    temp += np.random.normal(0, 0.5, n)
    
    # Humidity: 45-90%, inverse correlation with temp + monsoon bump
    humidity = diurnal_cycle(indices, -15.0, 65.0, phase_shift=0.3 + np.pi)
    # Monsoon bump (days 50-80 approximately)
    monsoon = 15 * sigmoid_ramp(indices / SAMPLES_PER_DAY, 50, 0.5) * \
              (1 - sigmoid_ramp(indices / SAMPLES_PER_DAY, 80, 0.5))
    humidity += monsoon + np.random.normal(0, 2.0, n)
    humidity = np.clip(humidity, 35, 98)
    
    # Pressure: 995-1015 hPa, slow variation
    pressure = diurnal_cycle(indices, 3.0, 1005.0, phase_shift=1.5)
    pressure += seasonal_drift(indices, n, 5.0)
    pressure += np.random.normal(0, 0.8, n)
    
    # === INJECT BLAST EVENTS ===
    blast_mask = np.zeros(n, dtype=int)
    for day, hour, duration_samples in BLAST_EVENTS:
        blast_start = day * SAMPLES_PER_DAY + hour * (60 // SAMPLE_INTERVAL_MIN)
        blast_end = min(blast_start + duration_samples, n)
        if blast_start < n:
            # Blast: high vibration spike, broadband freq, NO tilt/strain change
            vib_rms[blast_start:blast_end] = np.random.uniform(0.5, 1.5, 
                                                                blast_end - blast_start)
            vib_peak[blast_start:blast_end] = np.random.uniform(1.0, 2.5, 
                                                                  blast_end - blast_start)
            vib_freq[blast_start:blast_end] = np.random.uniform(25, 80, 
                                                                  blast_end - blast_start)
            blast_mask[blast_start:blast_end] = 1
    
    # === GENERATE LABELS ===
    labels = np.zeros(n, dtype=int)
    for i in range(n):
        day = i // SAMPLES_PER_DAY
        if blast_mask[i]:
            labels[i] = 3  # blast
        elif day < NORMAL_END or i < pre_sub_start_s:
            labels[i] = 0  # normal
        elif day < PRE_SUBSIDENCE_END:
            labels[i] = 1  # pre-subsidence
        elif day < ACTIVE_END:
            labels[i] = 2  # active subsidence
        else:
            # Post-active: still elevated but stabilizing
            labels[i] = 2 if influence > 0.5 else 1
    
    # === COMPUTE DERIVED FEATURES ===
    tilt_magnitude = np.sqrt(tilt_x**2 + tilt_y**2)
    
    # Tilt rate: diff over window (approximation)
    tilt_rate = np.zeros(n)
    tilt_rate[1:] = np.diff(tilt_magnitude)
    
    # Temp-humidity index (combined environmental feature)
    temp_norm = (temp - 20) / 25       # normalize to ~0-1
    hum_norm = (humidity - 35) / 65    # normalize to ~0-1
    temp_humidity_index = 0.5 * temp_norm + 0.5 * hum_norm
    
    # === BUILD TIMESTAMPS ===
    start_time = datetime(2026, 1, 1, 0, 0, 0)
    timestamps = [start_time + timedelta(minutes=SAMPLE_INTERVAL_MIN * i) for i in range(n)]
    
    # === ASSEMBLE DATAFRAMES ===
    raw_df = pd.DataFrame({
        'timestamp': timestamps,
        'node_id': node_id,
        'tilt_x_deg': np.round(tilt_x, 5),
        'tilt_y_deg': np.round(tilt_y, 5),
        'strain_delta_ue': np.round(strain_delta, 3),
        'vib_rms_g': np.round(vib_rms, 5),
        'vib_peak_g': np.round(vib_peak, 5),
        'vib_dominant_freq_hz': np.round(vib_freq, 2),
        'crack_status': crack,
        'temperature_c': np.round(temp, 2),
        'humidity_pct': np.round(humidity, 2),
        'pressure_hpa': np.round(pressure, 2),
    })
    
    feature_df = pd.DataFrame({
        'timestamp': timestamps,
        'node_id': node_id,
        'tilt_mean': np.round(tilt_magnitude, 5),
        'tilt_rate': np.round(tilt_rate, 6),
        'strain_delta': np.round(strain_delta, 3),
        'vib_rms': np.round(vib_rms, 5),
        'vib_peak': np.round(vib_peak, 5),
        'vib_dominant_freq': np.round(vib_freq, 2),
        'crack_status': crack,
        'temp_humidity_index': np.round(temp_humidity_index, 4),
        'label': labels,
    })
    
    return raw_df, feature_df


def generate_full_dataset():
    """Generate dataset for all nodes and save to CSV."""
    
    print("=" * 70)
    print("Mine Subsidence Monitoring — Synthetic Dataset Generator")
    print("=" * 70)
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    
    all_raw = []
    all_features = []
    
    for node_id, pos in NODE_POSITIONS.items():
        influence = subsidence_influence(pos)
        delay = subsidence_onset_delay_days(influence)
        print(f"\n  Generating {node_id} | zone={pos['zone']} | "
              f"influence={influence:.3f} | onset_delay={delay}d")
        
        raw_df, feat_df = generate_node_data(node_id, pos, influence)
        all_raw.append(raw_df)
        all_features.append(feat_df)
    
    # Combine all nodes
    raw_combined = pd.concat(all_raw, ignore_index=True)
    feat_combined = pd.concat(all_features, ignore_index=True)
    
    # Sort by timestamp then node
    raw_combined = raw_combined.sort_values(['timestamp', 'node_id']).reset_index(drop=True)
    feat_combined = feat_combined.sort_values(['timestamp', 'node_id']).reset_index(drop=True)
    
    # Extract labels
    labels_df = feat_combined[['timestamp', 'node_id', 'label']].copy()
    
    # Node positions
    pos_df = pd.DataFrame([
        {'node_id': nid, 'x_m': pos['x'], 'y_m': pos['y'], 'zone': pos['zone']}
        for nid, pos in NODE_POSITIONS.items()
    ])
    
    # Save
    raw_path = os.path.join(output_dir, 'raw_sensor_data.csv')
    feat_path = os.path.join(output_dir, 'feature_vectors_per_node.csv')
    labels_path = os.path.join(output_dir, 'labels.csv')
    pos_path = os.path.join(output_dir, 'node_positions.csv')
    meta_path = os.path.join(output_dir, 'metadata.json')
    
    raw_combined.to_csv(raw_path, index=False)
    feat_combined.to_csv(feat_path, index=False)
    labels_df.to_csv(labels_path, index=False)
    pos_df.to_csv(pos_path, index=False)
    
    # Metadata
    metadata = {
        'generated_at': datetime.now().isoformat(),
        'seed': SEED,
        'panel_width_m': PANEL_WIDTH_M,
        'panel_length_m': PANEL_LENGTH_M,
        'num_nodes': NUM_NODES,
        'total_days': TOTAL_DAYS,
        'sample_interval_min': SAMPLE_INTERVAL_MIN,
        'samples_per_node': TOTAL_SAMPLES,
        'total_rows': len(feat_combined),
        'phases': {
            'normal': f'Day 0-{NORMAL_END}',
            'pre_subsidence': f'Day {NORMAL_END}-{PRE_SUBSIDENCE_END}',
            'active_subsidence': f'Day {PRE_SUBSIDENCE_END}-{ACTIVE_END}',
            'stabilization': f'Day {ACTIVE_END}-{TOTAL_DAYS}',
        },
        'blast_events': [
            {'day': d, 'hour': h, 'duration_samples': dur}
            for d, h, dur in BLAST_EVENTS
        ],
        'node_influences': {
            nid: round(subsidence_influence(pos), 3)
            for nid, pos in NODE_POSITIONS.items()
        },
        'label_encoding': {
            '0': 'normal',
            '1': 'pre_subsidence',
            '2': 'active_subsidence',
            '3': 'blast_event'
        }
    }
    
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    # Summary
    print(f"\n{'=' * 70}")
    print(f"  Dataset Generated Successfully!")
    print(f"{'=' * 70}")
    print(f"  Raw sensor data:     {len(raw_combined):,} rows -> {raw_path}")
    print(f"  Feature vectors:     {len(feat_combined):,} rows -> {feat_path}")
    print(f"  Labels:              {len(labels_df):,} rows -> {labels_path}")
    print(f"  Node positions:      {len(pos_df)} nodes -> {pos_path}")
    print(f"  Metadata:            {meta_path}")
    print(f"\n  Label Distribution:")
    for label, name in metadata['label_encoding'].items():
        count = (labels_df['label'] == int(label)).sum()
        pct = count / len(labels_df) * 100
        print(f"    {label} ({name}): {count:,} ({pct:.1f}%)")
    print()
    
    return raw_combined, feat_combined


if __name__ == '__main__':
    generate_full_dataset()
