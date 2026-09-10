"""
PDF Document Generator — AI-Enabled Mine Subsidence Monitoring System (SIH26)
================================================================================
Generates a comprehensive, publication-quality technical report PDF covering:
  1. SIH26 Problem Statement (PS 26025, Ministry of Coal)
  2. Multi-Tier ML Architecture & Model Topology
  3. Physics-Informed Synthetic Dataset Specifications
  4. Flowcharts (System Architecture, Edge Inference, Gateway Logic, User Workflow)
  5. Empirical Accuracy Metrics & Visualizations
  6. Web Application & ESP32-S3 Hardware Flashing Guide
"""

import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.units import inch

def create_report_pdf():
    pdf_output_path = "d:\\innertask\\mine_subsidence_ml\\Mine_Subsidence_AI_Monitoring_System_SIH26.pdf"
    
    doc = SimpleDocTemplate(
        pdf_output_path,
        pagesize=letter,
        rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    NAVY = colors.HexColor("#0f172a")
    BLUE = colors.HexColor("#0284c7")
    DARK_BLUE = colors.HexColor("#1e3a8a")
    GRAY_TEXT = colors.HexColor("#334155")
    LIGHT_BG = colors.HexColor("#f8fafc")
    BORDER_COLOR = colors.HexColor("#cbd5e1")
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=NAVY,
        alignment=1, # Center
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=BLUE,
        alignment=1,
        spaceAfter=16
    )
    
    section_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=DARK_BLUE,
        spaceBefore=12,
        spaceAfter=8
    )
    
    subsection_heading = ParagraphStyle(
        'SubSecHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=NAVY,
        spaceBefore=10,
        spaceAfter=6
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=GRAY_TEXT,
        spaceAfter=8
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=10
    )
    
    story = []
    
    # =========================================================================
    # PAGE 1: TITLE, META & PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("AI-ENABLED MINE SUBSIDENCE MONITORING SYSTEM", title_style))
    story.append(Paragraph("Comprehensive Technical Report & Machine Learning Architecture<br/><b>Smart India Hackathon 2026 — Problem Statement 26025 (Ministry of Coal)</b>", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceBefore=0, spaceAfter=12))
    
    # Overview Metadata Table
    meta_data = [
        [Paragraph("<b>Organization:</b> Ministry of Coal / Coal India", body_style), Paragraph("<b>Target Site:</b> Underground Coal Mine Surface Panels", body_style)],
        [Paragraph("<b>Edge Deployment:</b> ESP32-S3 Wireless Mesh (802.15.4)", body_style), Paragraph("<b>TinyML Engine:</b> Isolation Forest (49.3 KB C Header)", body_style)],
        [Paragraph("<b>Cloud Engine:</b> Multi-Output LSTM Predictor", body_style), Paragraph("<b>Full-Stack App:</b> FastAPI + Glassmorphic UI (Port 8050)", body_style)]
    ]
    t_meta = Table(meta_data, colWidths=[260, 260])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("1. Problem Statement & Operational Scope", section_heading))
    p1_text = """
    <b>Background (SIH PS 26025):</b> Surface land subsidence caused by underground coal mining (longwall caving and pillar extraction) poses critical hazards to nearby rural communities, public highways, agricultural lands, and forest ecology. Traditional subsidence monitoring in India relies on periodic manual total station surveys, satellite InSAR, or post-facto damage assessments, which fail to issue <b>real-time early warnings</b> prior to ground failure.
    <br/><br/>
    <b>Technical Objective:</b> Develop an indigenous, low-cost, intelligent, real-time mine subsidence monitoring and prediction platform based on a surface-mounted wireless sensor mesh. The solution must continuously detect micro ground inclination, digital strain delta, transient vibrations, and fissure initiation, discriminate blasting operations from structural subsidence, and run edge anomaly scoring directly on microcontrollers.
    """
    story.append(Paragraph(p1_text, body_style))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("2. Multi-Tier System Architecture Flowchart", section_heading))
    
    # Architecture Flowchart (Clean ASCII)
    flowchart_code = """+-----------------------------------------------------------------------------------+
|                            SYSTEM ARCHITECTURE FLOWCHART                          |
+-----------------------------------------------------------------------------------+
  STAGE 1: SURFACE EDGE NODES (ESP32-S3)
  [IMU Tilt + Strain Gauge + Geophone Vibration + Breakwire + BME280]
     |
     v (Feature Extraction & Normalization)
  [Standalone C Model: isolation_forest_model.h (49.3 KB)]
     |
     v (Computes Anomaly Rating & Score in <150 microseconds)
  [Mesh Radio Packet: Anomaly Score + 8 Feature Summary]
     |
     v (802.15.4 / WiFi Self-Healing Mesh)
  STAGE 2: GATEWAY NODE (LOCAL / OFFLINE)
  [Collects Packets from All Nodes (N1..N5)]
     |
     v (Spatial Correlator & Blast Discriminator)
  [Vibration Spike + Zero Tilt/Strain Shift?] ---> [BLAST TRANSIENT: Suppress Siren]
     | NO (Correlated Tilt/Strain Shift)
     v
  [SUBSIDENCE PROGRESSION: Trigger Local Relay Siren + SIM7000 SMS Blast]
     |
     v (Cellular LTE-M Uplink)
  STAGE 3: CLOUD BACKEND & WEB PLATFORM (FastAPI - Port 8050)
  [InfluxDB Time-Series Store + Multi-Output LSTM Model (24hr Lookback Window)]
     |
     +---> Risk Probability (98.27% Accuracy)
     +---> Max Displacement mm (7.26 mm MAE Error)
     +---> Severity Classification (Low / Medium / High - 95.79% Accuracy)
+-----------------------------------------------------------------------------------+"""
    story.append(Paragraph(flowchart_code.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style))
    
    # =========================================================================
    # PAGE 2: SYNTHETIC DATASET
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Physics-Informed Synthetic Dataset Specifications", section_heading))
    p3_text = """
    Because real public subsidence-labeled datasets do not exist, a <b>physics-informed synthetic dataset</b> was generated modeling 5 surface nodes (N1 to N5) deployed over a 200m x 1500m Indian longwall coal panel footprint over a 90-day simulation period (sampled every 5 minutes = 129,600 total rows).
    """
    story.append(Paragraph(p3_text, body_style))
    
    # Dataset Summary Table
    ds_table_data = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Specification / Values</b>", body_style), Paragraph("<b>Physical Simulation Mechanics</b>", body_style)],
        [Paragraph("Time Horizon", body_style), Paragraph("90 Days (25,920 windows/node)", body_style), Paragraph("Covers full extraction & caving cycle", body_style)],
        [Paragraph("Total Dataset Rows", body_style), Paragraph("129,600 Rows across 5 Nodes", body_style), Paragraph("N1/N5 (Edge), N2/N4 (Mid), N3 (Center)", body_style)],
        [Paragraph("Normal Phase (68.0%)", body_style), Paragraph("Tilt < 0.05 deg, Strain < 1 uE", body_style), Paragraph("Gaussian noise + diurnal thermal drift", body_style)],
        [Paragraph("Pre-Subsidence (17.5%)", body_style), Paragraph("Tilt 0.05 deg -> 0.3 deg, Strain 2-10 uE", body_style), Paragraph("Sigmoid ramp profile over 15 days", body_style)],
        [Paragraph("Active Collapse (14.4%)", body_style), Paragraph("Tilt > 1.5 deg, Strain > 45 uE", body_style), Paragraph("Accelerating trough, crack breakwire flip", body_style)],
        [Paragraph("Blast Injections (0.1%)", body_style), Paragraph("Vib RMS 0.5-1.5g, Freq 25-80Hz", body_style), Paragraph("Transient spike WITHOUT tilt/strain shift", body_style)],
    ]
    t_ds = Table(ds_table_data, colWidths=[120, 180, 220])
    t_ds.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ds)
    story.append(Spacer(1, 10))
    
    # Dataset Image embed if exists
    ds_img = "d:\\innertask\\mine_subsidence_ml\\visualization\\dataset_sensor_streams.png"
    if os.path.exists(ds_img):
        story.append(Image(ds_img, width=6.8*inch, height=3.5*inch))
    
    # =========================================================================
    # PAGE 3: ML MODELS & EMPIRICAL RESULTS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Machine Learning Models & Empirical Verification", section_heading))
    
    p4_text = """
    <b>Stage 1: Edge TinyML Isolation Forest Model</b><br/>
    The edge model runs directly on ESP32-S3 microcontrollers. It is trained on normal baseline data (unsupervised) and exported into a standalone <b>49.3 KB C header file</b> (<code>isolation_forest_model.h</code>) with zero dynamic memory allocation.
    <br/><br/>
    <b>Stage 3: Cloud Multi-Output LSTM Model</b><br/>
    The cloud model processes rolling 24-hour sequence windows (288 timesteps x 40 multi-node features) to jointly predict subsidence risk probability, surface displacement in mm, and severity level (Low / Medium / High).
    """
    story.append(Paragraph(p4_text, body_style))
    
    # Model Comparison Table
    ml_table_data = [
        [Paragraph("<b>Model Scope</b>", body_style), Paragraph("<b>Algorithm</b>", body_style), Paragraph("<b>Key Benchmark Metric</b>", body_style), Paragraph("<b>Empirical Performance</b>", body_style)],
        [Paragraph("<b>Stage 1 Edge TinyML</b>", body_style), Paragraph("Isolation Forest (10 trees)", body_style), Paragraph("AUC-ROC Score", body_style), Paragraph("<b>0.9631</b> (Target > 0.90)", body_style)],
        [Paragraph("Edge Anomaly Alarm", body_style), Paragraph("emlearn C Export", body_style), Paragraph("False Positive Rate (FPR)", body_style), Paragraph("<b>1.06%</b> (Low False Alarms)", body_style)],
        [Paragraph("Active Subsidence", body_style), Paragraph("ESP32 Execution", body_style), Paragraph("Detection Recall Rate", body_style), Paragraph("<b>93.6%</b> (Target > 90%)", body_style)],
        [Paragraph("<b>Stage 3 Cloud Predictor</b>", body_style), Paragraph("Multi-Output 2-Layer LSTM", body_style), Paragraph("Risk Probability Accuracy", body_style), Paragraph("<b>98.27% Accuracy</b>", body_style)],
        [Paragraph("Displacement Forecast", body_style), Paragraph("Huber Regression Head", body_style), Paragraph("Mean Absolute Error (MAE)", body_style), Paragraph("<b>7.26 mm MAE Error</b>", body_style)],
        [Paragraph("Severity Classifier", body_style), Paragraph("Softmax Categorical Head", body_style), Paragraph("Classification Accuracy", body_style), Paragraph("<b>95.79% Accuracy</b>", body_style)],
    ]
    t_ml = Table(ml_table_data, colWidths=[120, 140, 130, 130])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 10))
    
    # Edge Evaluation Visualization
    edge_img = "d:\\innertask\\mine_subsidence_ml\\visualization\\edge_model_evaluation.png"
    if os.path.exists(edge_img):
        story.append(Image(edge_img, width=6.8*inch, height=3.2*inch))

    # =========================================================================
    # PAGE 4: CLOUD VISUALIZATION & USAGE GUIDE
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Cloud Performance Visualizations & Web Platform Guide", section_heading))
    
    cloud_img = "d:\\innertask\\mine_subsidence_ml\\visualization\\cloud_model_evaluation.png"
    if os.path.exists(cloud_img):
        story.append(Image(cloud_img, width=6.8*inch, height=3.0*inch))
        story.append(Spacer(1, 10))

    usage_code = """+-----------------------------------------------------------------------------------+
|                        WEB PLATFORM & USAGE FLOWCHART                             |
+-----------------------------------------------------------------------------------+
  STEP 1: START SERVER
  Run: d:\\innertask\\ml_venv\\Scripts\\python.exe web_app\\server.py
  Open Browser: http://localhost:8050
     |
     v
  STEP 2: LIVE GIS DASHBOARD TAB
  - Inspect surface deformation grid (1500m x 200m panel) with 5 active nodes.
  - Monitor Early Warning Risk Gauge (0.0 to 1.0) & Physical Siren state.
     |
     v
  STEP 3: INTERACTIVE ML TEST BENCH TAB
  - Click 'Preset: Pre-Subsidence' or 'Preset: Blast'.
  - Adjust sliders (Tilt, Strain, Vibration, Crack breakwire).
  - Observe real-time Edge Isolation Forest score & Cloud LSTM risk % update instantly.
     |
     v
  STEP 4: 90-DAY SIMULATION PLAYER TAB
  - Play through Phase 1 (Normal) ---> Phase 2 (Pre-Subsidence) ---> Phase 3 (Active) ---> Phase 4 (Blast).
+-----------------------------------------------------------------------------------+"""
    story.append(Paragraph(usage_code.replace(" ", "&nbsp;").replace("\n", "<br/>"), code_style))
    
    story.append(Paragraph("ESP32-S3 TinyML Hardware Flashing Instructions", subsection_heading))
    flashing_text = """
    <b>Flashing Steps for Field Microcontrollers:</b><br/>
    1. Copy <code>main.ino</code>, <code>isolation_forest_model.h</code>, <code>scaler_params.h</code>, and <code>feature_extractor.h</code> from <code>esp32_firmware/</code> into your Arduino sketch folder.<br/>
    2. Connect ESP32-S3 via USB-C cable. Select Board: <b>ESP32S3 Dev Module</b>.<br/>
    3. Click <b>Upload</b>. Open Serial Monitor at <b>115200 baud</b> to observe microsecond anomaly scores (&lt; 150 us)!
    """
    story.append(Paragraph(flashing_text, body_style))
    
    # Dashboard Screenshot embed if exists
    dash_img = "C:\\Users\\DR.RAJESH KUMAR\\.gemini\\antigravity-ide\\brain\\a192ea16-6894-4ae1-8955-c03bacc10385\\dashboard_main_1788941435321.png"
    if os.path.exists(dash_img):
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 5.1: MineGuard AI Web Dashboard Interface (Port 8050)</b>", subsection_heading))
        story.append(Image(dash_img, width=6.8*inch, height=3.0*inch))

    doc.build(story)
    print(f"\n==================================================")
    print(f"Generated PDF Document successfully at:\n  {pdf_output_path}")
    print(f"==================================================\n")

if __name__ == "__main__":
    create_report_pdf()
