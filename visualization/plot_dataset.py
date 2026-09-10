"""
Visualization — Plot Synthetic Dataset Sensor Streams
======================================================
Plots raw sensor channels and features across 90 days for all nodes.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_dataset_overview():
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    feat_path = os.path.join(base_dir, 'dataset', 'feature_vectors_per_node.csv')
    raw_path = os.path.join(base_dir, 'dataset', 'raw_sensor_data.csv')
    viz_dir = os.path.join(base_dir, 'visualization')
    os.makedirs(viz_dir, exist_ok=True)
    
    if not os.path.exists(feat_path):
        print(f"Dataset not found at {feat_path}")
        return
        
    df = pd.read_csv(feat_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filter for center node N3 and edge node N1
    n3 = df[df['node_id'] == 'N3'].sort_values('timestamp').reset_index(drop=True)
    n1 = df[df['node_id'] == 'N1'].sort_values('timestamp').reset_index(drop=True)
    
    days = (n3['timestamp'] - n3['timestamp'].min()).dt.total_seconds() / (24 * 3600)
    
    fig, axes = plt.subplots(4, 1, figsize=(15, 12), sharex=True)
    fig.suptitle('Mine Subsidence Sensor Mesh — 90-Day Multi-Sensor Stream (SIH26)', fontsize=16, fontweight='bold')
    
    # Subplot 1: Tilt Progression
    ax = axes[0]
    ax.plot(days, n3['tilt_mean'], label='N3 (Center - Max Subsidence)', color='#e74c3c', linewidth=1.5)
    ax.plot(days, n1['tilt_mean'], label='N1 (Edge - Lower Subsidence)', color='#3498db', linewidth=1.5)
    ax.axvspan(0, 60, color='green', alpha=0.1, label='Normal Phase')
    ax.axvspan(60, 75, color='yellow', alpha=0.15, label='Pre-Subsidence')
    ax.axvspan(75, 85, color='red', alpha=0.15, label='Active Subsidence')
    ax.set_ylabel('Tilt Angle (deg)')
    ax.set_title('Ground Tilt Surface Deformation Progression')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Subplot 2: Microstrain Delta
    ax = axes[1]
    ax.plot(days, n3['strain_delta'], color='#e67e22', label='N3 Strain Delta (µε)')
    ax.plot(days, n1['strain_delta'], color='#9b59b6', label='N1 Strain Delta (µε)')
    ax.set_ylabel('Strain (µε)')
    ax.set_title('Digital Strain Gauge Tensile/Compressive Stress Delta')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Subplot 3: Vibration RMS & Blast Injections
    ax = axes[2]
    ax.plot(days, n3['vib_rms'], color='#2ecc71', label='Vibration RMS (g)')
    ax.set_ylabel('Vibration RMS (g)')
    ax.set_title('Surface Vibration & Injected Transient Blast Signatures')
    ax.legend(loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    # Subplot 4: Crack Sensor Status
    ax = axes[3]
    ax.step(days, n3['crack_status'], color='#c0392b', label='N3 Crack Breakwire (1=Intact, 0=Broken)')
    ax.step(days, n1['crack_status'], color='#2980b9', label='N1 Crack Breakwire')
    ax.set_xlabel('Timeline (Days)')
    ax.set_ylabel('Status')
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Broken', 'Intact'])
    ax.set_title('Crack Breakwire Continuity State')
    ax.legend(loc='lower left')
    ax.grid(True, linestyle=':', alpha=0.6)
    
    plt.tight_layout()
    plot_path = os.path.join(viz_dir, 'dataset_sensor_streams.png')
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Saved dataset overview plot to {plot_path}")

if __name__ == '__main__':
    plot_dataset_overview()
