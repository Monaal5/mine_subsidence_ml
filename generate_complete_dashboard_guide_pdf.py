"""
Generate MineTrac Complete Dashboard & Voice Notes Master Guide PDF (SIH26)
=============================================================================
Creates a comprehensive multi-page PDF document in Hinglish & English explaining
every single button, card, ML model layer, scenario, voice script, and hardware deployment step.
"""

import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

def generate_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_filename = os.path.join(base_dir, "MineTrac_Complete_Dashboard_VoiceNotes_Guide_SIH26.pdf")
    
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Color Palette
    NAVY = colors.HexColor("#0f172a")       # Dark Primary Header
    SKY = colors.HexColor("#0284c7")        # Secondary Accent
    RED = colors.HexColor("#dc2626")        # Alert Red
    GREEN = colors.HexColor("#16a34a")      # Safe Green
    GOLD = colors.HexColor("#d97706")       # Warning Gold
    PURPLE = colors.HexColor("#9333ea")     # Blast Purple
    TEXT_DARK = colors.HexColor("#1e293b")  # Body Text
    TEXT_MUTED = colors.HexColor("#475569") # Secondary Text
    BG_CARD = colors.HexColor("#f8fafc")    # Card Fill
    BG_BOX = colors.HexColor("#f1f5f9")     # Callout Fill
    BORDER_CLR = colors.HexColor("#cbd5e1") # Divider Line
    CODE_BG = colors.HexColor("#0f172a")    # Dark Code Fill

    # Paragraph Styles
    doc_title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=18, leading=22,
        textColor=NAVY, alignment=TA_CENTER
    )

    doc_subtitle_style = ParagraphStyle(
        'DocSubtitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=SKY, alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'H1_Custom', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=13, leading=16,
        textColor=NAVY, spaceBefore=12, spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'H2_Custom', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=SKY, spaceBefore=8, spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=TEXT_DARK, alignment=TA_JUSTIFY, spaceBefore=2, spaceAfter=3
    )

    voice_style = ParagraphStyle(
        'Voice_Script', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9, leading=13.5,
        textColor=colors.HexColor("#0f172a"), alignment=TA_LEFT, spaceBefore=3, spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Style', parent=styles['Normal'],
        fontName='Courier', fontSize=8, leading=10.5,
        textColor=colors.HexColor("#38bdf8"), alignment=TA_LEFT
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("MineTrac AI — Dashboard & Voice Notes Master Guide (SIH26)", doc_title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("Complete Technical Breakdown, Minute Button Details, 3-Tier ML Pipeline & Word-for-Word Hinglish Voice Scripts", doc_subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=SKY, spaceBefore=2, spaceAfter=10))

    # Executive Overview Callout
    intro_html = (
        "<b>📌 Purpose of this Master Guide:</b><br/>"
        "Yeh document aapki poori team aur dosto ke liye ek comprehensive reference runbook hai. "
        "Isme MineTrac Dashboard ke **har minute button**, **card**, **underground schematic**, **Leaflet map**, "
        "**3-Tier ML model prediction logic**, **4 longwall scenarios**, **word-for-word Hinglish voice scripts**, "
        "aur **ESP32 hardware deployment steps** ko deep detail me explain kiya gaya hai."
    )
    elements.append(Paragraph(intro_html, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 1: TOP BAR & DASHBOARD HEADER BUTTONS
    elements.append(Paragraph("1. Dashboard Header & Minute Button Breakdown", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    topbar_html = (
        "<b>1. Logo & Team Branding:</b><br/>"
        "• <b>MineTrac Logo:</b> <code>MineTrac BY AKSSAI ProjExcel | SIH26 Coalition</code>. AI-driven underground mining risk platform branding.<br/><br/>"

        "<b>2. Header Control Buttons (Minute Detail):</b><br/>"
        "• <code>📊 Reports</code> Button: Opens a modal generating downloadable PDF & CSV compliance audit logs for Directorate General of Mines Safety (DGMS).<br/>"
        "• <code>🌐 All Mesh Nodes</code> Button: Opens a grid modal displaying individual hardware status, RSSI radio strength, and battery voltage of Nodes N1–N5.<br/>"
        "• <code>🛡️ Safety Rules</code> Button: Displays DGMS safety thresholds (Max allowable tilt = 0.5°, Max strain = 15 µε).<br/>"
        "• <code>⚙️ Master Config</code> Button: Adjusts Gateway polling frequency (1s to 5min) and SMS notification phone numbers.<br/>"
        "• <code>🔇 Audio Siren: MUTED / ACTIVE</code> Button: Controls Web Audio API synthesizer. When active during Critical Subsidence (Phase 3), fires a dual-tone emergency siren.<br/>"
        "• <code>👤 User Badge: Justin Humphrey</code>: Displays current logged-in role (Safety Director, Jharia Coalfield Panel 4).<br/><br/>"

        "<b>3. Secondary Navigation Tabs:</b><br/>"
        "• <code>Dashboard</code>: Primary operational cockpit displaying live KPIs, schematic, GIS map, and early warning gauge.<br/>"
        "• <code>ML Test Bench (3-Tier ML)</code>: Interactive ML playground with 8 sensor sliders for testing Edge, Gateway, and Cloud model inferences live.<br/>"
        "• <code>90-Day Simulation & Scenarios</code>: Time-series playback of the 4 longwall extraction phases (50 windows).<br/>"
        "• <code>Hardware & Flashing Guide</code>: Hardware pinout diagrams and Arduino C source code."
    )
    elements.append(Paragraph(topbar_html, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 2: TOP KPI CARDS & TEST PRESET BUTTONS
    elements.append(Paragraph("2. Top KPI Summary Cards & Test Presets Bar", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    kpi_html = (
        "<b>Top KPI Summary Cards:</b><br/>"
        "• <b>Active Mesh Nodes (5/5 Online):</b> Shows 100% 802.15.4 mesh radio connectivity. If a node loses power/signal for >30s, status updates to <i>Offline/Stale</i>.<br/>"
        "• <b>Max Surface Tilt (0.02°):</b> Live ground inclination angle calculated from MPU6050 accelerometer. Baseline = 0.02°.<br/>"
        "• <b>Max Strain Stress Delta (0.5 µε):</b> Microstrain delta from digital strain gauge. Baseline = 0.5 µε.<br/>"
        "• <b>Subsidence Risk % (2.4% SAFE_STABLE / 12.0% BLAST_FILTERED):</b> AI-calculated collapse probability.<br/><br/>"

        "<b>Test Presets Bar (1-Click Scenario Simulation):</b><br/>"
        "• <code>Case 1: Normal Operation</code>: Safe baseline (Tilt 0.02°, Strain 0.5 µε, Vib 0.025g, Risk 2.4%).<br/>"
        "• <code>Case 2: Pre-Subsidence Creep</code>: Monotonic tilt ramp (0.05° → 0.35°), strain bump (8.5 µε), Risk 45.0%.<br/>"
        "• <code>Case 3: Active Subsidence</code>: Rapid collapse (Tilt 1.45°, Strain 32 µε, Breakwire broken), Siren fires, Risk 94.2%.<br/>"
        "• <code>Case 4: Explosive Blasting</code>: High vibration spike (1.45g) with ZERO tilt/strain shift. Blast Filtered!<br/>"
        "• <code>Case 5: Breakwire Trip</code>: Direct physical fissure rupture detection."
    )
    elements.append(Paragraph(kpi_html, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 3: UNDERGROUND SCHEMATIC & GIS MAP
    elements.append(Paragraph("3. Underground Longwall Schematic & GIS Satellite Map", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    schematic_html = (
        "<b>Underground Longwall Mine Cutaway Schematic:</b><br/>"
        "• <b>Surface Layer:</b> Coal Preparation Plant, Raw-Coal Silo, Elevator Shaft Head, and 5 Surface Sensor Pins (Slave N1 to N5) spaced over 1500m × 200m grid.<br/>"
        "• <b>Strata Layer:</b> Overburden Sandstone & Shale Strata. Transmits underground roof collapse strain upwards.<br/>"
        "• <b>Underground Layer:</b> Elevator Shaft, Haulage Slope, <b>GOB ZONE (Collapsed Roof Void)</b>, Hydraulic Roof Support Shearer, Continuous Miner, and Coal Pillars.<br/>"
        "• <b>Dynamic Visualization:</b> As ground deformation occurs, GOB zone borders and surface node pins dynamically transition from Green → Amber → Red.<br/><br/>"

        "<b>GIS Satellite Map (Leaflet.js + Esri World Imagery):</b><br/>"
        "• Pinpoints nodes N1–N5 on actual Jharia Coalfield GPS coordinates.<br/>"
        "• Node N3 represents the center max-stress zone.<br/>"
        "• Clicking any node marker opens a live popup with pitch, roll, tilt, vibration RMS, battery voltage, and TinyML score.<br/>"
        "• <b>Color Legend:</b> 🟢 Normal | 🟡 Pre-Subsidence | 🔴 Active Alert | 🟣 Blast Filtered"
    )
    elements.append(Paragraph(schematic_html, body_style))
    elements.append(Spacer(1, 10))

    # PAGE BREAK FOR ML PIPELINE & VOICE SCRIPTS
    elements.append(PageBreak())

    # SECTION 4: 3-TIER ML MODEL ARCHITECTURE & PREDICTION LOGIC
    elements.append(Paragraph("4. Three-Tier ML Model Architecture & Prediction Logic", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    ml_table_data = [
        [Paragraph("<b>ML Stage & Layer</b>", body_style), Paragraph("<b>Model Type & Framework</b>", body_style), Paragraph("<b>Execution Speed & Function</b>", body_style)],
        [
            Paragraph("<b>Stage 1: Edge TinyML</b><br/>(ESP32-S3 Node)", body_style),
            Paragraph("<b>Isolation Forest</b><br/>Compiled C Header (<code>isolation_forest_model.h</code>)", body_style),
            Paragraph("<b>101.3 µs</b> execution.<br/>Evaluates 8 scaled feature vectors. Normalized score <code>s = -2^(-avg_depth / c(n))</code>. Flags score < -0.6127.", body_style)
        ],
        [
            Paragraph("<b>Stage 2: Gateway Correlator</b><br/>(Master Gateway)", body_style),
            Paragraph("<b>Spatial-Temporal Rules Engine</b><br/>Adjacent Node Correlator", body_style),
            Paragraph("Evaluates spatial multi-node consensus. Detects high vibration with ZERO tilt/strain → <code>OPERATIONAL BLAST (FILTERED)</code>, suppressing siren.", body_style)
        ],
        [
            Paragraph("<b>Stage 3: Cloud LSTM</b><br/>(Render Cloud)", body_style),
            Paragraph("<b>Multi-Output LSTM</b><br/>TensorFlow Keras (24hr window)", body_style),
            Paragraph("Predicts Subsidence Probability %, Max Displacement (mm), and Severity Class (LOW / MEDIUM / HIGH).", body_style)
        ]
    ]

    ml_table = Table(ml_table_data, colWidths=[130, 180, 230])
    ml_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_BOX),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(ml_table)
    elements.append(Spacer(1, 10))

    # SECTION 5: WORD-FOR-WORD HINGLISH VOICE NOTE SCRIPTS
    elements.append(Paragraph("5. Word-for-Word Hinglish Voice Note Scripts (Voice 1 to 7)", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    vn_1 = (
        "<b>🎙️ Voice Note 1: Top Navigation & Executive Introduction</b><br/>"
        "<i>\"Hello everyone! Welcome to MineTrac AI. Yeh humara low-cost, real-time mine subsidence detection, prediction, aur early warning platform hai jo Smart India Hackathon (SIH26) ke problem statement ke liye develop kiya gaya hai. "
        "Top bar par aap mine location dropdown dekh sakte hain jo abhi Jharia Coalfield Longwall Panel 4 ko monitor kar raha hai. "
        "Yahan active navigation tabs hain—Dashboard, 3-Tier ML Test Bench, 90-Day Simulation Timeline, aur Hardware Flashing Guide. "
        "Right side par audio siren control abhi Muted state me hai aur safety director badge gateway connectivity verify karta hai.\"</i>"
    )
    elements.append(Paragraph(vn_1, voice_style))
    elements.append(Spacer(1, 5))

    vn_2 = (
        "<b>🎙️ Voice Note 2: Top KPI Metric Cards & Test Preset Buttons</b><br/>"
        "<i>\"Top KPI cards par focus karte hain: Pehla card hai Active Mesh Nodes, jo dikhata hai ki hamare 5 me se 5 nodes online hain aur 100% radio signal ke saath connected hain. "
        "Doosra card hai Max Surface Tilt jo 0.02 degrees par hai—yeh hamara normal safe baseline hai. "
        "Teesra card hai Max Strain Stress Delta jo 0.5 microstrain par normal tensile strain dikhata hai. "
        "Chautha card hai Subsidence Risk Percentage jo 2.4% par Safe Stable status dikha raha hai. "
        "Directly neeche 5 quick test preset buttons hain jisse hum Normal, Pre-Subsidence, Active Collapse, aur Dynamite Blasting scenarios ko 1-click me test kar sakte hain.\"</i>"
    )
    elements.append(Paragraph(vn_2, voice_style))
    elements.append(Spacer(1, 5))

    vn_3 = (
        "<b>🎙️ Voice Note 3: Underground Mine Cutaway Schematic</b><br/>"
        "<i>\"Yeh middle section me hamara anatomical underground longwall mine cross-section visualizer hai. "
        "Top surface par hamare preparation plant, coal silo, elevator shaft head, aur 1500m × 200m surface grid par Slave N1 se Slave N5 tak ke 5 sensor pins mounted hain. "
        "Neeche overburden sandstone aur shale strata layers hain jo underground ground deformation ko surface tak transmit karti hain. "
        "Sabse neeche underground area me GOB Zone—yaani collapsed roof void—hydraulic roof support shearer, aur coal pillars dikhaye gaye hain. "
        "Jaise hi underground caving start hoti hai, surface pins aur GOB zone border ka color real-time dynamic update hota hai.\"</i>"
    )
    elements.append(Paragraph(vn_3, voice_style))
    elements.append(Spacer(1, 5))

    vn_4 = (
        "<b>🎙️ Voice Note 4: GIS Satellite Map & Node Mesh Overlay</b><br/>"
        "<i>\"Neeche left side par hamara Surface Panel GIS Map hai jo High-Definition Esri World Imagery Satellite Tiles use karta hai. "
        "Yeh map Jharia Coalfield ke actual GPS coordinates par surface sensor nodes ko pinpoint karta hai. "
        "Node N3 center max-stress zone par positioned hai. Marker par click karne se node ka real-time tilt, strain, vibration, battery, aur TinyML isolation forest status popup me khul jaata hai. "
        "Ground risk ke aadhar par color dots green, yellow, red, ya purple me transform ho jaate hain.\"</i>"
    )
    elements.append(Paragraph(vn_4, voice_style))
    elements.append(Spacer(1, 5))

    vn_5 = (
        "<b>🎙️ Voice Note 5: Gateway Early Warning Status & Blast Filter</b><br/>"
        "<i>\"Bottom right side par hamara Master Gateway Early Warning Status panel hai jo 0.0 se 1.0 ke scale par live subsidence risk score dikhata hai. "
        "Jab underground dynamite blasting hoti hai, toh traditional sensors false alarm trigger kar dete hain aur mining ko faltu me rokna padta hai. "
        "Lekin hamara Stage 2 Gateway Spatial Correlator detect karta hai ki high vibration ke saath TILT 0 hai. "
        "Ise yeh OPERATIONAL BLAST (FILTERED) classify karke physical siren ko suppress kar deta hai, jisse false alarm rukta hai aur mining bina kisi rukaawat ke chalti rehti hai!\"</i>"
    )
    elements.append(Paragraph(vn_5, voice_style))
    elements.append(Spacer(1, 5))

    vn_6 = (
        "<b>🎙️ Voice Note 6: Interactive 3-Tier ML Test Bench & Sliders</b><br/>"
        "<i>\"Ab hum ML Test Bench tab par hain. Yahan Node N3 ke 8 physical sensor sliders—Tilt Mean, Tilt Rate, Strain Delta, Vibration RMS, Peak, Frequency, aur Crack Breakwire—ko live manipulate kar sakte hain. "
        "Right side par hamara 3-Tier ML Model inference result dikhata hai:<br/>"
        "1. Stage 1 Edge TinyML (ESP32-S3) Isolation Forest C model ko 86.4 microseconds me execute karta hai.<br/>"
        "2. Stage 2 Gateway Correlator adjacent nodes ka spatial correlation aur blast suppression evaluate karta hai.<br/>"
        "3. Stage 3 Cloud Multi-Output LSTM (TensorFlow Keras) 24-hour sequence window se surface displacement millimeters me aur severity class predict karta hai.\"</i>"
    )
    elements.append(Paragraph(vn_6, voice_style))
    elements.append(Spacer(1, 5))

    vn_7 = (
        "<b>🎙️ Voice Note 7: 90-Day Indian Longwall Mining Timeline (Phase 1 - 4)</b><br/>"
        "<i>\"Finally, hamare 90-Day Simulation tab me hum Longwall Extraction ke pure 4 geomechanical phases ko 50 time-series windows me play back karte hain:<br/>"
        "• Phase 1 (Normal, Days 0-60): Flat baseline ground (Tilt 0.02°, Risk 2.4%).<br/>"
        "• Phase 2 (Pre-Subsidence Creep, Days 60-75): Overburden micro-cracking, steady tilt ramp (0.05° → 0.37°), rising strain (14.5 µε), triggering early warning at 45% risk.<br/>"
        "• Phase 3 (Active Collapse, Days 75-85): Main roof falls into GOB void, rapid tilt acceleration (>1.5°), strain spike (58 µε), breakwire flip, triggering 94.2% risk & siren alert! 🚨<br/>"
        "• Phase 4 (Dynamite Blast Event): Explosive vibration spikes to 1.45g while tilt stays ZERO (0.02°), demonstrating blast false-alarm suppression.\"</i>"
    )
    elements.append(Paragraph(vn_7, voice_style))
    elements.append(Spacer(1, 10))

    # SECTION 6: REMOTE DEPLOYMENT GUIDE (GHAR + HARDWARE TEAM)
    elements.append(Paragraph("6. Remote Deployment Guide (Ghar + On-Site Hardware Team)", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    dep_guide = (
        "<b>🏠 AAP (Ghar Par - Remote Developer):</b><br/>"
        "1. Github repository <code>https://github.com/Monaal5/mine_subsidence_ml.git</code> par code updated hai.<br/>"
        "2. <b>Render.com</b> par New Web Service banakar GitHub connect karein. Docker select karke Deploy par click karein.<br/>"
        "3. 2 minute me Render aapko public link dega: <code>https://mine-subsidence-ml-2rr5.onrender.com</code>.<br/>"
        "4. Modifies RAM usage under 200MB & dynamic PORT binding fixes free-tier memory issues!<br/><br/>"

        "<b>🔧 HARDWARE TEAM (On-Site Location):</b><br/>"
        "1. <b>ESP32-S3 Sensor Nodes Flashing:</b> ESP32-S3 ko USB se laptop me connect karein. Arduino IDE me <code>esp32_firmware/slave_node.ino</code> aur <code>master_gateway.ino</code> kholein.<br/>"
        "2. Flash Master Gateway first, get its MAC address from Serial log, paste into Slave Node <code>masterAddress[]</code> array, and flash Slave.<br/>"
        "3. Turn on Phone Hotspot WiFi — both nodes connect automatically and stream live hardware telemetry to the cloud dashboard!"
    )
    elements.append(Paragraph(dep_guide, body_style))
    elements.append(Spacer(1, 14))

    # Footer
    footer_p = ParagraphStyle(
        'FooterP', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY, alignment=TA_CENTER
    )
    elements.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceBefore=4, spaceAfter=6))
    elements.append(Paragraph("MineTrac AI Mining Platform © 2026 | Built for Smart India Hackathon (SIH26)", footer_p))

    doc.build(elements)
    print(f"PDF Generated Successfully at: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
