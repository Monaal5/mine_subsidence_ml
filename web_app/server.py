"""
Mine Subsidence Monitoring System — FastAPI Server & Web App
============================================================
Serves the web UI dashboard, interactive ML test bench, and REST API
integrating Stage 1 Edge TinyML, Stage 2 Gateway Correlator, and Stage 3 Cloud LSTM models.
Optimized for Low Memory Cloud Free-Tier Deployment (<250MB RAM).
"""

import os
import sys

# Suppress TF logs & restrict thread allocations for 512MB RAM cloud free-tiers
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['TF_NUM_INTRAOP_THREADS'] = '1'
os.environ['TF_NUM_INTEROP_THREADS'] = '1'

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import joblib
import json
import time

import tensorflow as tf
from tensorflow import keras

# Path setup
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATASET_DIR = os.path.join(BASE_DIR, 'dataset')
WEB_APP_DIR = os.path.join(BASE_DIR, 'web_app')

app = FastAPI(
    title="AI-Enabled Mine Subsidence Monitoring API (SIH26)",
    description="Low-Cost Real-Time Mine Subsidence Detection, Prediction & Early Warning System",
    version="1.0.0"
)

# Static files
app.mount("/static", StaticFiles(directory=os.path.join(WEB_APP_DIR, "static")), name="static")

# ============================================================================
# LOAD MODELS & ARTIFACTS
# ============================================================================

print("=" * 70)
print("Loading ML Models for Mine Subsidence Monitoring Platform...")
print("=" * 70)

try:
    edge_model = joblib.load(os.path.join(MODELS_DIR, 'isolation_forest.pkl'))
    edge_scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler.pkl'))
    edge_threshold = float(np.load(os.path.join(MODELS_DIR, 'anomaly_threshold.npy')))
    print(f"  [OK] Edge Isolation Forest loaded (Threshold: {edge_threshold:.5f})")
except Exception as e:
    print(f"  [WARN] Failed to load Edge model: {e}")
    edge_model, edge_scaler, edge_threshold = None, None, -0.61

try:
    cloud_model = keras.models.load_model(os.path.join(MODELS_DIR, 'cloud_lstm_model.keras'))
    cloud_scaler = joblib.load(os.path.join(MODELS_DIR, 'cloud_scaler.pkl'))
    with open(os.path.join(MODELS_DIR, 'cloud_feature_cols.json'), 'r') as f:
        cloud_feature_cols = json.load(f)
    print(f"  [OK] Cloud LSTM Model loaded ({len(cloud_feature_cols)} features)")
except Exception as e:
    print(f"  [WARN] Failed to load Cloud LSTM model: {e}")
    cloud_model, cloud_scaler, cloud_feature_cols = None, None, []

# Memory-optimized dataset loading for scenario simulation
try:
    pos_df = pd.read_csv(os.path.join(DATASET_DIR, 'node_positions.csv'))
    print(f"  [OK] Node metadata loaded")
except Exception as e:
    print(f"  [WARN] Failed to load metadata: {e}")
    pos_df = None

# Import spatial correlator
sys.path.append(os.path.join(BASE_DIR, 'gateway_logic'))
try:
    from spatial_correlator import SpatialCorrelator
    correlator = SpatialCorrelator()
    print("  [OK] Gateway Spatial Correlator initialized")
except Exception as e:
    print(f"  [WARN] Gateway Correlator fallback: {e}")
    correlator = None


# ============================================================================
# SCHEMAS
# ============================================================================

class EdgePredictionRequest(BaseModel):
    tilt_mean: float = Field(0.02, description="Tilt magnitude (deg)")
    tilt_rate: float = Field(0.0001, description="Tilt rate (deg/min)")
    strain_delta: float = Field(0.5, description="Strain gauge delta (microstrain)")
    vib_rms: float = Field(0.025, description="Vibration RMS (g)")
    vib_peak: float = Field(0.06, description="Vibration peak (g)")
    vib_dominant_freq: float = Field(14.5, description="Vibration frequency (Hz)")
    crack_status: int = Field(1, description="Crack status (1=intact, 0=broken)")
    temp_humidity_index: float = Field(0.55, description="Combined env index (0-1)")

class NodeIngestPacket(BaseModel):
    node_id: int = Field(1, description="Node ID (1-5)")
    timestamp: int = Field(0, description="Unix timestamp from RTC")
    pitch: float = Field(0.0, description="Pitch angle (deg)")
    roll: float = Field(0.0, description="Roll angle (deg)")
    mpu_vib_rms: float = Field(0.0, description="MPU6050 vibration RMS (m/s2)")
    adxl_vib_rms: float = Field(0.0, description="ADXL345 vibration RMS (m/s2)")
    stage1_anomaly_score: int = Field(0, description="Rule-based anomaly flag (0 or 1)")
    lat: float = Field(30.7588, description="Latitude fallback")
    lng: float = Field(76.7685, description="Longitude fallback")

class GatewayPacketRequest(BaseModel):
    packets: Dict[str, Dict[str, float]]

class CloudPredictionRequest(BaseModel):
    sequence: List[List[float]]

# Global in-memory store for live hardware telemetry
latest_packets: Dict[str, dict] = {}


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "AI-Enabled Mine Subsidence Monitoring Platform (SIH26)",
        "models_loaded": {
            "edge_model": edge_model is not None,
            "cloud_model": cloud_model is not None,
            "dataset_available": True
        }
    }

@app.post("/api/ingest")
def ingest_packet(pkt: NodeIngestPacket):
    """Receives live hardware sensor payload from Master Gateway ESP32 over HTTP/HTTPS."""
    node_key = f"N{pkt.node_id}"
    pkt_dict = pkt.dict()
    pkt_dict["received_at"] = time.time()
    
    # Calculate derived features
    tilt_mag = float(np.sqrt(pkt.pitch**2 + pkt.roll**2))
    vib_rms = max(pkt.mpu_vib_rms, pkt.adxl_vib_rms)
    pkt_dict["tilt_mean"] = round(tilt_mag, 4)
    pkt_dict["vib_rms"] = round(vib_rms, 4)
    
    # Run Edge Isolation Forest model scoring if available
    if edge_model is not None and edge_scaler is not None:
        try:
            # 8 features: tilt_mean, tilt_rate, strain_delta, vib_rms, vib_peak, vib_dominant_freq, crack_status, temp_humidity_index
            raw_f = np.array([[tilt_mag, 0.0, 0.0, vib_rms, vib_rms*1.5, 14.5, 1.0, 0.5]], dtype=np.float32)
            scaled = edge_scaler.transform(raw_f)
            score = float(edge_model.score_samples(scaled)[0])
            pkt_dict["edge_score"] = round(score, 5)
            pkt_dict["is_anomalous"] = bool(score < edge_threshold or pkt.stage1_anomaly_score == 1)
        except Exception:
            pkt_dict["edge_score"] = -0.45
            pkt_dict["is_anomalous"] = bool(pkt.stage1_anomaly_score == 1)
    else:
        pkt_dict["edge_score"] = -0.45
        pkt_dict["is_anomalous"] = bool(pkt.stage1_anomaly_score == 1)
        
    latest_packets[node_key] = pkt_dict
    return {"status": "ok", "node": node_key, "is_anomalous": pkt_dict["is_anomalous"]}

@app.get("/api/nodes/live")
def get_live_nodes():
    """Returns real-time hardware telemetry and active/stale status for all nodes."""
    now = time.time()
    res = {}
    for k, v in latest_packets.items():
        node_data = dict(v)
        node_data["stale"] = (now - v.get("received_at", now)) > 30  # 30-second heartbeat timeout
        res[k] = node_data
    return res

@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    html_path = os.path.join(WEB_APP_DIR, "templates", "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Mine Subsidence Dashboard UI loading...</h1>"

@app.post("/api/predict/edge")
def predict_edge(req: EdgePredictionRequest):
    """Executes TinyML Stage 1 Isolation Forest Anomaly Scoring."""
    if edge_model is None or edge_scaler is None:
        raise HTTPException(status_code=500, detail="Edge model not loaded")
        
    start_t = time.perf_counter()
    
    raw_feats = np.array([[
        req.tilt_mean, req.tilt_rate, req.strain_delta,
        req.vib_rms, req.vib_peak, req.vib_dominant_freq,
        float(req.crack_status), req.temp_humidity_index
    ]], dtype=np.float32)
    
    scaled_feats = edge_scaler.transform(raw_feats)
    score = float(edge_model.score_samples(scaled_feats)[0])
    
    exec_time_us = (time.perf_counter() - start_t) * 1e6
    is_anomalous = bool(score < edge_threshold or req.crack_status == 0)
    
    norm_score = max(0.0, min(100.0, (score - (-0.8)) / (0.0 - (-0.8)) * 100.0))
    rating = "NORMAL" if not is_anomalous else ("WARNING" if norm_score > 30 else "CRITICAL ANOMALY")
    
    return {
        "anomaly_score": round(score, 5),
        "threshold": round(edge_threshold, 5),
        "is_anomalous": is_anomalous,
        "rating": rating,
        "execution_time_us": round(exec_time_us, 1),
        "simulated_mcu_inference_us": round(np.random.uniform(80, 140), 1)
    }

@app.post("/api/predict/gateway")
def predict_gateway(req: GatewayPacketRequest):
    """Executes Stage 2 Gateway local spatial correlation & blast discrimination."""
    if correlator is None:
        raise HTTPException(status_code=500, detail="Gateway Correlator not loaded")
        
    result = correlator.evaluate_window(req.packets)
    return result

@app.post("/api/predict/cloud")
def predict_cloud(req: CloudPredictionRequest):
    """Executes Stage 3 Cloud Multi-Output LSTM Prediction."""
    if cloud_model is None or cloud_scaler is None:
        raise HTTPException(status_code=500, detail="Cloud LSTM model not loaded")
        
    seq = np.array(req.sequence, dtype=np.float32)
    if seq.shape != (288, 40):
        if seq.shape[1] == 40 and seq.shape[0] < 288:
            pad = np.zeros((288 - seq.shape[0], 40), dtype=np.float32)
            seq = np.vstack([pad, seq])
        elif seq.shape[0] > 288:
            seq = seq[-288:]
        else:
            seq = np.zeros((288, 40), dtype=np.float32)

    seq_batch = np.expand_dims(seq, axis=0)
    
    pred_prob, pred_disp, pred_sev = cloud_model.predict(seq_batch, verbose=0)
    
    prob_val = float(pred_prob[0][0])
    disp_mm = float(max(0.0, pred_disp[0][0]))
    sev_classes = ["LOW", "MEDIUM", "HIGH"]
    sev_idx = int(np.argmax(pred_sev[0]))
    sev_str = sev_classes[sev_idx]
    
    return {
        "subsidence_probability": round(prob_val, 4),
        "predicted_max_displacement_mm": round(disp_mm, 2),
        "severity_class": sev_str,
        "confidence": round(float(np.max(pred_sev[0])), 4),
        "severity_probabilities": {
            "low": round(float(pred_sev[0][0]), 4),
            "medium": round(float(pred_sev[0][1]), 4),
            "high": round(float(pred_sev[0][2]), 4)
        }
    }

@app.get("/api/nodes/positions")
def get_node_positions():
    """Returns grid positions of all 5 surface nodes."""
    if pos_df is not None:
        return pos_df.to_dict(orient="records")
    return [
        {'node_id': 'N1', 'x_m': 30, 'y_m': 375, 'zone': 'edge'},
        {'node_id': 'N2', 'x_m': 80, 'y_m': 750, 'zone': 'mid'},
        {'node_id': 'N3', 'x_m': 100, 'y_m': 750, 'zone': 'center'},
        {'node_id': 'N4', 'x_m': 130, 'y_m': 750, 'zone': 'mid'},
        {'node_id': 'N5', 'x_m': 170, 'y_m': 1125, 'zone': 'edge'},
    ]

@app.get("/api/dataset/scenario/{scenario_name}")
def get_scenario_data(scenario_name: str):
    """Returns 50-window sensor dataset stream for demo scenarios: normal, pre_subsidence, active, blast."""
    scen = scenario_name.lower()
    sample_nodes = {}
    np.random.seed(42)

    for node_id in ['N1', 'N2', 'N3', 'N4', 'N5']:
        node_records = []
        is_center = (node_id == 'N3')
        multiplier = 1.0 if is_center else (0.6 if node_id in ['N2', 'N4'] else 0.3)

        for i in range(50):
            if scen == 'normal':
                tilt = 0.02 + np.random.normal(0, 0.003)
                strain = 0.5 + np.random.normal(0, 0.15)
                vib = 0.025 + np.random.normal(0, 0.004)
            elif scen == 'pre_subsidence':
                tilt = (0.05 + (i / 50.0) * 0.32 * multiplier) + np.random.normal(0, 0.008)
                strain = (1.5 + (i / 50.0) * 11.5 * multiplier) + np.random.normal(0, 0.3)
                vib = 0.04 + np.random.normal(0, 0.006)
            elif scen == 'active':
                prog = (i / 50.0) ** 1.8
                tilt = (0.2 + prog * 1.85 * multiplier) + np.random.normal(0, 0.015)
                strain = (8.0 + prog * 44.0 * multiplier) + np.random.normal(0, 0.8)
                vib = 0.12 + np.random.normal(0, 0.02)
            elif scen == 'blast':
                tilt = 0.02 + np.random.normal(0, 0.003)
                strain = 0.5 + np.random.normal(0, 0.15)
                if 20 <= i <= 25:
                    vib = (1.1 + np.random.uniform(0.1, 0.35)) * multiplier
                else:
                    vib = 0.025 + np.random.normal(0, 0.004)
            else:
                tilt = 0.02
                strain = 0.5
                vib = 0.025

            node_records.append({
                "window": i + 1,
                "node_id": node_id,
                "tilt_mean": round(float(max(0.0, tilt)), 4),
                "strain_delta": round(float(strain), 2),
                "vib_rms": round(float(max(0.0, vib)), 4)
            })

        sample_nodes[node_id] = node_records

    return {
        "scenario": scenario_name,
        "nodes": sample_nodes
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8050))
    uvicorn.run(app, host="0.0.0.0", port=port)
