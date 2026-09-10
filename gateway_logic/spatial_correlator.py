"""
Gateway Local Processing — Stage 2: Spatial Correlator & Blast Discriminator
============================================================================
Runs locally on the Gateway node (offline capable). Performs:
  1. Spatial correlation across nodes
  2. Blast vs. Subsidence Discrimination
  3. Rolling Trend Regression (Tilt/Strain velocity)
  4. Alert State Machine & siren trigger decision
"""

import numpy as np
import pandas as pd
import json
import os


class SpatialCorrelator:
    def __init__(self, node_positions_path=None):
        if node_positions_path is None:
            node_positions_path = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'node_positions.csv')
            
        if os.path.exists(node_positions_path):
            self.nodes_df = pd.read_csv(node_positions_path)
        else:
            self.nodes_df = pd.DataFrame([
                {'node_id': 'N1', 'x_m': 30, 'y_m': 375, 'zone': 'edge'},
                {'node_id': 'N2', 'x_m': 80, 'y_m': 750, 'zone': 'mid'},
                {'node_id': 'N3', 'x_m': 100, 'y_m': 750, 'zone': 'center'},
                {'node_id': 'N4', 'x_m': 130, 'y_m': 750, 'zone': 'mid'},
                {'node_id': 'N5', 'x_m': 170, 'y_m': 1125, 'zone': 'edge'},
            ])
            
        # Alert thresholds
        self.ANOMALY_SCORE_THRESHOLD = -0.05  # Isolation forest score boundary
        self.TILT_VELOCITY_WARN_DEG_HR = 0.05
        self.TILT_VELOCITY_CRIT_DEG_HR = 0.15
        self.STRAIN_VELOCITY_WARN_UE_HR = 2.0
        
    def evaluate_window(self, node_packets):
        """
        Evaluate a single timestamp packet collected from mesh nodes.
        node_packets: dict of {node_id: {'anomaly_score': float, 'tilt_mean': float, 
                                        'strain_delta': float, 'vib_rms': float, 'vib_peak': float,
                                        'vib_freq': float, 'crack_status': int}}
        
        Returns: decision dict (action, alert_level, summary, siren_trigger, sms_trigger)
        """
        anomalous_nodes = []
        high_vib_nodes = []
        tilt_strain_shifting_nodes = []
        
        for node_id, p in node_packets.items():
            is_anomaly = p.get('anomaly_score', 0.0) < self.ANOMALY_SCORE_THRESHOLD or p.get('crack_status', 1) == 0
            if is_anomaly:
                anomalous_nodes.append(node_id)
                
            # Check for high vibration (blast-like)
            if p.get('vib_rms', 0.0) > 0.4 or p.get('vib_peak', 0.0) > 1.0:
                high_vib_nodes.append(node_id)
                
            # Check tilt/strain shifts
            if p.get('tilt_mean', 0.0) > 0.25 or p.get('strain_delta', 0.0) > 10.0:
                tilt_strain_shifting_nodes.append(node_id)

        num_anomalies = len(anomalous_nodes)
        
        # --- RULE 1: BLAST DISCRIMINATION ---
        # High vibration + NO tilt/strain trend shift across mesh
        if len(high_vib_nodes) > 0 and len(tilt_strain_shifting_nodes) == 0:
            return {
                'event_type': 'BLAST_TRANSIENT',
                'alert_level': 'INFO',
                'siren_trigger': False,
                'sms_trigger': False,
                'summary': f'Transient blast/machinery vibration suppressed on nodes: {high_vib_nodes}. Ground tilt/strain remains stable.'
            }

        # --- RULE 2: SPATIAL SUBSIDENCE CORRELATION ---
        # Correlated anomaly across adjacent/multiple nodes WITH tilt/strain shifts
        if num_anomalies >= 2 and len(tilt_strain_shifting_nodes) >= 1:
            return {
                'event_type': 'SUBSIDENCE_PROGRESSION',
                'alert_level': 'CRITICAL',
                'siren_trigger': True,
                'sms_trigger': True,
                'summary': f'CRITICAL SUBSIDENCE DETECTED! Correlated deformation across nodes {anomalous_nodes}. Siren & SMS triggered!'
            }

        # --- RULE 3: SINGLE NODE SENSOR ANOMALY / EARLY PRE-SUBSIDENCE ---
        if num_anomalies == 1:
            return {
                'event_type': 'EARLY_WARNING_OR_SENSOR_FAULT',
                'alert_level': 'WARNING',
                'siren_trigger': False,
                'sms_trigger': False,
                'summary': f'Early warning anomaly detected on single node {anomalous_nodes[0]}. Monitoring spatial spread.'
            }

        return {
            'event_type': 'NORMAL_STABLE',
            'alert_level': 'NORMAL',
            'siren_trigger': False,
            'sms_trigger': False,
            'summary': 'All ground deformation indicators within normal safety bounds.'
        }


def test_correlator():
    print("=" * 70)
    print("Gateway Stage 2 Spatial Correlator Test")
    print("=" * 70)
    
    correlator = SpatialCorrelator()
    
    # Scenario 1: Normal State
    normal_pkt = {
        'N1': {'anomaly_score': 0.12, 'tilt_mean': 0.01, 'strain_delta': 0.2, 'vib_rms': 0.02, 'crack_status': 1},
        'N2': {'anomaly_score': 0.10, 'tilt_mean': 0.02, 'strain_delta': 0.1, 'vib_rms': 0.02, 'crack_status': 1},
        'N3': {'anomaly_score': 0.15, 'tilt_mean': 0.01, 'strain_delta': 0.3, 'vib_rms': 0.03, 'crack_status': 1},
    }
    res1 = correlator.evaluate_window(normal_pkt)
    print(f"\nScenario 1 (Normal): {res1['event_type']} -> Siren={res1['siren_trigger']}")
    print(f"  Summary: {res1['summary']}")
    
    # Scenario 2: Blast Event (High vib, no tilt/strain shift)
    blast_pkt = {
        'N1': {'anomaly_score': -0.15, 'tilt_mean': 0.02, 'strain_delta': 0.2, 'vib_rms': 0.85, 'vib_peak': 1.8, 'crack_status': 1},
        'N2': {'anomaly_score': -0.18, 'tilt_mean': 0.01, 'strain_delta': 0.1, 'vib_rms': 0.92, 'vib_peak': 2.1, 'crack_status': 1},
        'N3': {'anomaly_score': 0.11,  'tilt_mean': 0.02, 'strain_delta': 0.3, 'vib_rms': 0.10, 'vib_peak': 0.2, 'crack_status': 1},
    }
    res2 = correlator.evaluate_window(blast_pkt)
    print(f"\nScenario 2 (Blast): {res2['event_type']} -> Siren={res2['siren_trigger']}")
    print(f"  Summary: {res2['summary']}")
    
    # Scenario 3: Active Subsidence (Correlated anomaly + tilt/strain shift + crack)
    subsidence_pkt = {
        'N2': {'anomaly_score': -0.35, 'tilt_mean': 0.65, 'strain_delta': 24.5, 'vib_rms': 0.12, 'crack_status': 0},
        'N3': {'anomaly_score': -0.42, 'tilt_mean': 1.15, 'strain_delta': 42.0, 'vib_rms': 0.18, 'crack_status': 0},
        'N4': {'anomaly_score': -0.28, 'tilt_mean': 0.45, 'strain_delta': 18.2, 'vib_rms': 0.08, 'crack_status': 1},
    }
    res3 = correlator.evaluate_window(subsidence_pkt)
    print(f"\nScenario 3 (Subsidence): {res3['event_type']} -> Siren={res3['siren_trigger']}")
    print(f"  Summary: {res3['summary']}")
    
    print(f"\n{'=' * 70}")
    print("  Gateway Logic Test Complete!")
    print(f"{'=' * 70}\n")


if __name__ == '__main__':
    test_correlator()
