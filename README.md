# Mine Subsidence AI Monitoring Platform (SIH26)

Real-Time Mine Subsidence Detection, Prediction & Early Warning System integrating 3-Tier ML (Stage 1 Edge TinyML, Stage 2 Gateway Correlator, Stage 3 Cloud LSTM).

## Features
- **Stage 1 Edge TinyML**: Isolation Forest C Header running on ESP32-S3 microcontrollers (~112 µs execution speed).
- **Stage 2 Gateway Correlator**: Spatial correlation & operational blast discrimination.
- **Stage 3 Cloud LSTM**: TensorFlow Keras spatial-temporal subsidence probability & displacement prediction.
- **Web App Dashboard**: Interactive real-time dashboard built with FastAPI, Leaflet GIS map API, and Chart.js.

## Quick Start
```bash
python -m venv ml_venv
ml_venv\Scripts\activate
pip install -r requirements.txt
python web_app/server.py
```
Open `http://localhost:8050` in browser.
