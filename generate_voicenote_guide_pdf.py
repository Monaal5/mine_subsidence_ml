"""
PDF Generator — Voice-Note Script & Detailed Graph Breakdown Guide (Hinglish)
=============================================================================
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

def create_voicenote_pdf():
    pdf_path = r"d:\innertask\mine_subsidence_ml\Mine_Subsidence_VoiceNote_Explanation_Guide.pdf"
    
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    # Palette
    NAVY = colors.HexColor("#0f172a")
    BLUE = colors.HexColor("#0284c7")
    DARK_BLUE = colors.HexColor("#1e3a8a")
    GRAY_TEXT = colors.HexColor("#334155")
    BORDER_COLOR = colors.HexColor("#cbd5e1")
    PURPLE = colors.HexColor("#6b21a8")
    
    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY,
        alignment=1,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=BLUE,
        alignment=1,
        spaceAfter=10
    )
    
    sec_heading = ParagraphStyle(
        'SecHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=DARK_BLUE,
        spaceBefore=8,
        spaceAfter=5
    )
    
    subsec_heading = ParagraphStyle(
        'SubSecHeading',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=NAVY,
        spaceBefore=6,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=GRAY_TEXT,
        spaceAfter=5
    )

    voicenote_style = ParagraphStyle(
        'VoiceNoteText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=NAVY,
        backColor=colors.HexColor("#f8fafc"),
        borderColor=colors.HexColor("#cbd5e1"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9.5,
        textColor=NAVY,
        backColor=colors.HexColor("#f1f5f9"),
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=4,
        spaceAfter=5
    )
    
    story = []
    
    # Title Header
    story.append(Paragraph("MINE SUBSIDENCE ML — VOICE-NOTE EXPLANATION & GRAPH GUIDE", title_style))
    story.append(Paragraph("Complete Hinglish Voice-Note Script for Friends, Master/Slave Architecture, Graphs & Backend Breakdown", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=BLUE, spaceBefore=0, spaceAfter=6))
    
    # -------------------------------------------------------------------------
    # SECTION 1: VOICE-NOTE SCRIPT PART 1 - CONCEPT & ARCHITECTURE
    # -------------------------------------------------------------------------
    story.append(Paragraph("🎙️ Voice-Note Script — Part 1: High-Level Concept & Master/Slave Architecture", sec_heading))
    
    vn_p1 = """
    <b>"Hey Bhai/Dosto! Suno, main poore Mine Subsidence Monitoring project ka concept ekdum simple hinglish mein samjhata hoon:</b><br/><br/>
    <b>1. Problem Kya Hai?</b><br/>
    Underground coal mines mein jab neeche se koyla nikala jata hai, toh oopar ki zameen (surface) bina kisi alert ke अचानक dhas jaati hai (Subsidence). Iss se zameen par chal rahe trucks, buildings aur human lives khatre mein aate hain. Manual survey slow hote hain aur Satellite InSAR 12 din late alert deta hai.<br/><br/>
    <b>2. Humne Kya Solution Banaya?</b><br/>
    Humne ek 3-Stage IoT + AI System banaya hai jisme **Slave Nodes**, **Master Node (Gateway)**, aur **Cloud Server** aapas mein mil kar kaam karte hain:<br/><br/>
    • <b>Slave Nodes (Sensor Nodes N1 se N5):</b> Zameen par field mein 5 alag points par <b>ESP32 Microcontrollers</b> lage hain. Har Slave Node par 5 sensors hain (Tilt IMU, Strain Gauge, Vibration Geophone, Crack Tripwire, aur Temp/Humidity). Ye har 10 millisecond mein readings lete hain aur iske andar C-language mein chota sa ML model (<b>Isolation Forest</b>) chalta hai. Ye instantly pata kar leta hai ki local zameen mein koi anomaly/stress toh nahi hai. Phir ye radio mesh (ESP-NOW) se data Master Node ko bhejte hain.<br/><br/>
    • <b>Master Node (Gateway Node):</b> Ye central hub hai. Iska sabse zaroori kaam hai <b>Mining Blasts ko Filter karna!</b> Jab mine mein controlled blasting hoti hai, toh poori mine mein ek saath jhatka lagta hai. Master Node saare Slave Nodes (N1..N5) ka data correlate karta hai. Agar vibration poore area mein ek saath aayi hai without tilt -> toh ye isko BLAST samajhta hai aur false siren suppress kar deta hai. Agar vibration ke saath center nodes (N2, N3, N4) par tilt aur strain badh raha hai -> toh ye REAL SUBSIDENCE ALERT trigger kar deta hai!<br/><br/>
    • <b>Cloud Server:</b> Master Node har 24 ghante ka data cellular LTE se Cloud ko bhejta hai. Cloud par humara <b>Deep Learning LSTM Neural Network</b> chalta hai jo agle 24-48 ghante ka prediction deta hai: Kitne % risk hai, kitne millimeter zameen dhasaegi, aur risk level (Low, Medium, High) kya hai!"
    """
    story.append(Paragraph(vn_p1, voicenote_style))
    story.append(Spacer(1, 4))

    # -------------------------------------------------------------------------
    # SECTION 2: DATASET EXPLANATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("🎙️ Voice-Note Script — Part 2: Dataset Explanation in Hinglish", sec_heading))
    
    vn_p2 = """
    <b>"Ab suno humare Dataset ke baare mein:</b><br/><br/>
    Real mine failure ka continuous public dataset available nahi hota. Isliye humne ek **Physics-Based Geomechanical Simulator** banaya jo 90 days ka continuous sensor telemetry generate karta hai across 5 spatial nodes (N1 to N5) har 5 minute par (Total 129,600 rows).<br/><br/>
    Dataset mein 4 realistic phases hain:<br/>
    1. <b>Normal Phase (Day 0 - 60):</b> Zameen shaant hai. Tilt 0 degree, strain 0 microstrain, crack breakwire intact (1) hai.<br/>
    2. <b>Pre-Subsidence Creep (Day 60 - 75):</b> Zameen dhiere-dhiere jhukna shuru hoti hai (Tilt 0.05° se 0.5° badhta hai) aur strain stress 0 se 15 microstrain tak badhta hai.<br/>
    3. <b>Active Subsidence (Day 75 - 90):</b> Zameen tezi se dhasti hai! Tilt >1.5° se 2.1° cross kar jata hai, strain 45 microstrain touch karta hai, aur Day 80 par physical crack breakwire 1 se drop hokar 0 (Broken) ho jata hai!<br/>
    4. <b>Blasting Spikes:</b> Controlled mining explosions jisme sudden 1.4g vibration spikes aate hain without tilt creep."
    """
    story.append(Paragraph(vn_p2, voicenote_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SECTION 3: DETAILED GRAPH BREAKDOWN
    # -------------------------------------------------------------------------
    story.append(Paragraph("📊 Detailed Explanation of All 3 Evaluation Graphs & Visualizations", sec_heading))
    
    story.append(Paragraph("📷 Graph 1: Cloud Model (LSTM) Evaluation Plots (cloud_model_evaluation.png)", subsec_heading))
    
    cloud_graph_text = """
    <b>1. Displacement Estimation Plot (Top-Left):</b><br/>
    • <b>X-axis:</b> Actual Displacement in mm (0 to 150 mm). <b>Y-axis:</b> Predicted Displacement in mm.<br/>
    • <b>Red Dashed Line:</b> Ye ideal 1:1 perfect prediction line hai.<br/>
    • <b>Scatter Dots:</b> Blue dots red dashed line ke bilkul paas cluster kar rahe hain. Model ka **Mean Absolute Error (MAE) = 7.26 mm** hai! Iska matlab humara Cloud LSTM model zameen ke dhasne ki depth sub-centimeter (7mm margin) accuracy se predict kar raha hai.<br/><br/>
    <b>2. Severity Confusion Matrix (Top-Right):</b><br/>
    • 3x3 Heatmap Grid for Low, Medium, and High Severity classification.<br/>
    • <b>Low Severity:</b> 1,416 samples correctly predicted as Low! (Sirf 1 medium aur 1 high misclassify hua).<br/>
    • <b>Medium Severity:</b> 325 samples correctly predicted as Medium.<br/>
    • <b>High Severity (CRITICAL):</b> 305 samples correctly predicted as High! **0 high-risk events were predicted as Low!** Iska matlab system kabhi bhi dangerous collapse ko safe nahi bataega — Zero Critical False Negatives!<br/><br/>
    <b>3. Cloud Risk Trajectory Over Time (Bottom-Left):</b><br/>
    • <b>X-axis:</b> Sequence Window Index (Time timeline). <b>Y-axis:</b> Risk Probability (0.0 to 1.0).<br/>
    • Day 0 se Day 60 tak (Index 0 to 1450), Risk Curve flat **0.02** par rehti hai (Normal safe state).<br/>
    • Index 1450 (Day 60 - Pre-Subsidence creep onset) par risk curve sharp vertical jump leti hai aur **1.0 (100% Risk)** touch karti hai. Dashed warning line (0.5) cross karte hi Control Room dashboard par Red Siren baj jata hai — giving hours/days of advance warning!<br/><br/>
    <b>4. Displacement Error Distribution (Bottom-Right):</b><br/>
    • Residual Error = (Actual Displacement - Predicted Displacement).<br/>
    • Green histogram peak bilkul **0.0 mm** par centered hai with a narrow bell curve. Ye prove karta hai ki model unbiased hai (na ziada predict karta hai na kam).
    """
    story.append(Paragraph(cloud_graph_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("📷 Graph 2: Edge Model (Isolation Forest) Evaluation Plots (edge_model_evaluation.png)", subsec_heading))
    
    edge_graph_text = """
    <b>1. Score Distribution Plot (Top-Left):</b><br/>
    • Green Distribution = Normal baseline telemetry (Scores centered around -0.45).<br/>
    • Red Distribution = Anomaly telemetry (Scores centered around -0.68).<br/>
    • Orange Dashed Line = **Anomaly Threshold at -0.613**.<br/>
    • Agar score > -0.613 hai toh Normal hai; agar score < -0.613 hai toh Edge Microcontroller Anomaly flag karta hai!<br/><br/>
    <b>2. ROC Curve Plot (Top-Right):</b><br/>
    • Trade-off between False Positive Rate and True Positive Rate.<br/>
    • Blue curve top-left corner se touch hoke ja rahi hai with **AUC = 0.9631 (96.31%)**. Extremely strong edge detection capability!<br/><br/>
    <b>3. Anomaly Scores Over Time - Node N3 Center (Bottom-Left):</b><br/>
    • 90-Day timeline plot for Center Slave Node N3.<br/>
    • Day 0 to 60: Green dots normal range (-0.40 to -0.50) mein hain.<br/>
    • Day 60 (Pre-subsidence start): Orange dots sharp drop dikhate hain aur red threshold line (-0.613) ke neeche gir kar -0.73 touch karte hain!<br/>
    • Day 75 to 90 (Active Subsidence): Red dots constantly threshold ke neeche rehte hain.<br/><br/>
    <b>4. Confusion Matrix (Bottom-Right):</b><br/>
    • **True Normal (TN):** 87,149 instances correctly classified as Normal.<br/>
    • **True Anomaly (TP):** 32,412 instances correctly classified as Anomalies directly on ESP32 Microcontrollers in microseconds!
    """
    story.append(Paragraph(edge_graph_text, body_style))
    story.append(Spacer(1, 4))

    story.append(Paragraph("📷 Graph 3: 90-Day Sensor Mesh Streams (dataset_sensor_streams.png)", subsec_heading))
    
    mesh_graph_text = """
    <b>1. Ground Tilt Surface Deformation (Subplot 1):</b> Red line (Center Node N3) vs Blue line (Edge Node N1). Day 60 tak tilt 0° hai. Day 60-75 (Yellow zone) mein N3 tilt 0.5° tak badhta hai. Day 75+ (Red zone) mein N3 tilt **2.1°** touch kar leta hai (Max Subsidence), jabki edge node N1 sirf 0.5° tak jata hai.<br/>
    <b>2. Digital Strain Gauge Stress Delta (Subplot 2):</b> Orange line (N3) strain stress **45 microstrain** tak shoot hota hai tensile stretching ke wajah se.<br/>
    <b>3. Vibration & Blasting (Subplot 3):</b> Green line shows 5 sharp vertical spikes up to **1.4g acceleration** (operational blasting events).<br/>
    <b>4. Crack Breakwire Continuity State (Subplot 4):</b> Red line (N3) Day 80 par **1 (Intact) se drop hokar 0 (Broken)** ho jati hai jab zameen physical crack open karti hai!
    """
    story.append(Paragraph(mesh_graph_text, body_style))

    story.append(PageBreak())

    # -------------------------------------------------------------------------
    # SECTION 4: BACKEND API & HOW MODELS PREDICT
    # -------------------------------------------------------------------------
    story.append(Paragraph("🎙️ Voice-Note Script — Part 3: Backend APIs & How Models Predict", sec_heading))
    
    vn_p3 = """
    <b>"Ab suno Backend APIs aur Models kaam kaise karte hain:</b><br/><br/>
    Backend FastAPI (Python) par chalta hai port 8050 par. Isme 3 main prediction endpoints hain:<br/><br/>
    <b>1. Edge API (`POST /api/predict/edge`):</b><br/>
    Slave Node apna 8-feature payload bhejta hai (`tilt_mean`, `strain_delta`, `vib_rms`, `crack_status` etc.).<br/>
    • **Prediction Mechanism:** Isolation Forest model baseline normal features se distance calculate karta hai. Agar score < -0.613 hai ya crack_status == 0 hai, toh response aata hai: `is_anomalous: true`, `rating: CRITICAL ANOMALY`, execution time `<150 microseconds`!<br/><br/>
    <b>2. Gateway API (`POST /api/predict/gateway`):</b><br/>
    Master Node 5 Slave Nodes (N1 se N5) ke packets bhejta hai.<br/>
    • **Prediction Mechanism:** Gateway Spatial Correlator check karta hai ki kya vibration pure mesh mein hai without tilt creep? If YES -> Response: `is_blast: true`, `suppress_alarm: true`. If NO (tilt creep present) -> Response: `subsidence_alert: true`.<br/><br/>
    <b>3. Cloud API (`POST /api/predict/cloud`):</b><br/>
    Cloud ko 24-hour sequence matrix (288 timesteps x 40 features) bheji jaati hai.<br/>
    • **Prediction Mechanism:** Deep Multi-Output LSTM model sequence process karke 3 parallel outputs generate karta hai:<br/>
      - `subsidence_probability`: e.g. 0.8924 (89.24% Risk)<br/>
      - `predicted_max_displacement_mm`: e.g. 42.5 mm depth<br/>
      - `severity_class`: HIGH (Low/Med/High severity)<br/><br/>
    <b>Summary for Friends:** Slave node INSTANT alert deta hai, Master node FALSE ALARM filter karta hai, aur Cloud LSTM FUTURE RISK & DISPLACEMENT predict karta hai! Point to point complete solution!"</b>
    """
    story.append(Paragraph(vn_p3, voicenote_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("💻 Commands to Run Backend & Test Dashboard", sec_heading))
    run_cmd = """<b>Command to Start Server:</b><br/>
<code>d:\\innertask\\ml_venv\\Scripts\\python.exe d:\\innertask\\mine_subsidence_ml\\web_app\\server.py</code>
<br/><br/>
<b>Access Points:</b><br/>
• Dashboard: <font color="#0284c7"><u>http://localhost:8050/</u></font><br/>
• Swagger API Docs: <font color="#0284c7"><u>http://localhost:8050/docs</u></font><br/>
• API Health Check: <font color="#0284c7"><u>http://localhost:8050/api/health</u></font>"""
    story.append(Paragraph(run_cmd, body_style))

    doc.build(story)
    print(f"Successfully generated VoiceNote PDF Guide at: {pdf_path}")

if __name__ == "__main__":
    create_voicenote_pdf()
