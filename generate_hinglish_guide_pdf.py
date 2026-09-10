"""
Generate MineTrac Hinglish Complete Presentation & Voice Note Guide PDF
========================================================================
Creates a beautifully formatted PDF document in Hinglish explaining every dashboard component,
giving word-for-word voice note scripts, and detailing remote deployment.
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
    pdf_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MineTrac_Hinglish_Complete_Guide_SIH26.pdf")
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Color Palette
    PRIMARY = colors.HexColor("#0d4715")     # Deep Green
    SECONDARY = colors.HexColor("#e11d48")   # Brand Red
    ACCENT = colors.HexColor("#0284c7")      # Primary Blue
    GOLD = colors.HexColor("#d97706")        # Gold/Amber
    DARK_TEXT = colors.HexColor("#0f172a")   # Dark Navy Text
    MUTED_TEXT = colors.HexColor("#475569")  # Slate Gray
    BG_LIGHT = colors.HexColor("#f8fafc")    # Light Card
    BG_BOX = colors.HexColor("#f1f5f9")      # Box Fill
    BORDER_CLR = colors.HexColor("#cbd5e1")  # Border

    # Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=SECONDARY,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=ACCENT,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=DARK_TEXT,
        alignment=TA_JUSTIFY,
        spaceBefore=3,
        spaceAfter=3
    )

    voice_style = ParagraphStyle(
        'Voice_Script',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        alignment=TA_LEFT,
        spaceBefore=4,
        spaceAfter=4
    )

    elements = []

    # Title Banner
    elements.append(Paragraph("MineTrac AI — Mine Subsidence Monitoring Platform (SIH26)", title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("Complete Hinglish Speech & Voice Note Guide + Technical Explanation PDF", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=4, spaceAfter=12))

    # Introduction Box
    intro_html = (
        "<b>📌 Purpose of this Document (Hinglish Guide):</b><br/>"
        "Yeh PDF aapke presentation, voice notes recording, aur team hardware demo ke liye banaya gaya hai. "
        "Isme MineTrac Dashboard ke har ek section ka <b>detailed Hinglish explanation</b>, exact <b>word-for-word voice note scripts</b>, "
        "aur <b>remote deployment guide</b> (Aap ghar par + Hardware team on-site) fully explain kiya gaya hai."
    )
    elements.append(Paragraph(intro_html, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 1: DASHBOARD COMPONENTS EXPLANATION
    elements.append(Paragraph("1. Dashboard Ke Har Component Ka Step-by-Step Explanation (Hinglish)", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    comp_1 = (
        "<b>1. Top Header & Navigation Bar:</b><br/>"
        "• <b>Logo & Title:</b> <code>MineTrac BY AKSSAI ProjExcel | SIH26 Coalition</code>.<br/>"
        "• <b>Mine Location Selector:</b> Dropdown me <i>Jharia Coalfield — Longwall Panel 4</i> select karke kisi bhi mine area ka telemetry real-time dekh sakte hain.<br/>"
        "• <b>Audio Siren Toggle:</b> <code>Audio Siren: MUTED / ACTIVE</code> button. Emergency condition me physical high-decibel siren trigger hota hai.<br/>"
        "• <b>Secondary Tab Bar:</b> Dashboard, ML Test Bench (3-Tier ML), 90-Day Simulation & Scenarios, aur Hardware & Flashing Guide ke beech switch karne ke liye."
    )
    elements.append(Paragraph(comp_1, body_style))
    elements.append(Spacer(1, 6))

    comp_2 = (
        "<b>2. Top KPI Summary Metric Cards:</b><br/>"
        "• <b>Active Mesh Nodes (5/5 Online):</b> Sabhi 5 surface sensor nodes online hain aur 100% radio signal connectivity de rahe hain.<br/>"
        "• <b>Max Surface Tilt (0.02°):</b> Surface ground acceleration se calculat hone wala inclination angle. Normal baseline 0.02° hota hai.<br/>"
        "• <b>Max Strain Stress Delta (0.5 µε):</b> Rock mass ke andar digital strain gauge ka tensile stress delta.<br/>"
        "• <b>Subsidence Risk % (2.4% SAFE_STABLE):</b> AI model dwara calculated overall subsidence collapse probability."
    )
    elements.append(Paragraph(comp_2, body_style))
    elements.append(Spacer(1, 6))

    comp_3 = (
        "<b>3. Test Scenario Presets Bar (Quick Testing):</b><br/>"
        "• <b>Case 1 (Normal Operation):</b> Safe elastic ground, risk 2.4%.<br/>"
        "• <b>Case 2 (Pre-Subsidence Creep):</b> Slow monotonic tilt ramp (0.05° → 0.35°), risk 45.0%.<br/>"
        "• <b>Case 3 (Active Subsidence):</b> Ground collapse, rapid tilt (>1.5°), breakwire trip, siren fires, risk 94.2%.<br/>"
        "• <b>Case 4 (Explosive Blasting):</b> High RMS vibration spike (1.45g) zero tilt ke saath (blast suppressed!).<br/>"
        "• <b>Case 5 (Breakwire Trip):</b> Physical fissure rupture detection."
    )
    elements.append(Paragraph(comp_3, body_style))
    elements.append(Spacer(1, 6))

    comp_4 = (
        "<b>4. Underground Longwall Mine Cutaway Schematic:</b><br/>"
        "• <b>Surface Layer:</b> Preparation plant, Raw-Coal silo, Elevator shaft, aur 5 surface sensor pins (Slave N1 se Slave N5).<br/>"
        "• <b>Strata Layer:</b> Overburden sandstone aur shale layers, jo roof fall strain ko upar transmit karte hain.<br/>"
        "• <b>Underground Layer:</b> <i>GOB Zone</i> (collapsed roof void), Hydraulic roof support shearer, Continuous miner section, aur coal pillars."
    )
    elements.append(Paragraph(comp_4, body_style))
    elements.append(Spacer(1, 6))

    comp_5 = (
        "<b>5. GIS Satellite Map & Master Gateway Early Warning Status:</b><br/>"
        "• <b>Esri Satellite Map API:</b> Jharia Coalfield GPS grid par nodes N1-N5, Pits, aur Relay stations map par pinpoint hote hain.<br/>"
        "• <b>Blast Discrimination Filter:</b> Agar underground dynamite blast hota hai, toh high vibration aane par bhi tilt 0 rehta hai. Gateway ise <code>OPERATIONAL BLAST (FILTERED)</code> bolke false siren ko suppress kar deta hai!"
    )
    elements.append(Paragraph(comp_5, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 2: VOICE NOTE SPEECH SCRIPTS IN HINGLISH
    elements.append(Paragraph("2. Complete Voice Note Speech Scripts (Word-for-Word Hinglish)", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    vn_1 = (
        "<b>🎙️ Voice Note 1: Top Navigation & Executive Introduction</b><br/>"
        "<i>\"Hello everyone! Welcome to MineTrac AI. Yeh humara low-cost, real-time mine subsidence detection, prediction, aur early warning platform hai jo Smart India Hackathon (SIH26) ke problem statement ke liye develop kiya gaya hai. "
        "Top bar par aap mine location dropdown dekh sakte hain jo abhi Jharia Coalfield Longwall Panel 4 ko monitor kar raha hai. "
        "Yahan active navigation tabs hain—Dashboard, 3-Tier ML Test Bench, 90-Day Simulation Timeline, aur Hardware Flashing Guide. "
        "Right side par audio siren control abhi Muted state me hai aur safety director badge gateway connectivity verify karta hai.\"</i>"
    )
    elements.append(Paragraph(vn_1, voice_style))
    elements.append(Spacer(1, 6))

    vn_2 = (
        "<b>🎙️ Voice Note 2: Top KPI Metric Cards & Test Preset Buttons</b><br/>"
        "<i>\"Top KPI cards par focus karte hain: Pehla card hai Active Mesh Nodes, jo dikhata hai ki hamare 5 me se 5 nodes online hain aur 100% radio signal ke saath connected hain. "
        "Doosra card hai Max Surface Tilt jo 0.02 degrees par hai—yeh hamara normal safe baseline hai. "
        "Teesra card hai Max Strain Stress Delta jo 0.5 microstrain par normal tensile strain dikhata hai. "
        "Chautha card hai Subsidence Risk Percentage jo 2.4% par Safe Stable status dikha raha hai. "
        "Directly neeche 5 quick test preset buttons hain jisse hum Normal, Pre-Subsidence, Active Collapse, aur Dynamite Blasting scenarios ko 1-click me test kar sakte hain.\"</i>"
    )
    elements.append(Paragraph(vn_2, voice_style))
    elements.append(Spacer(1, 6))

    vn_3 = (
        "<b>🎙️ Voice Note 3: Underground Mine Cutaway Schematic</b><br/>"
        "<i>\"Yeh middle section me hamara anatomical underground longwall mine cross-section visualizer hai. "
        "Top surface par hamare preparation plant, coal silo, elevator shaft head, aur 1500m × 200m surface grid par Slave N1 se Slave N5 tak ke 5 sensor pins mounted hain. "
        "Neeche overburden sandstone aur shale strata layers hain jo underground ground deformation ko surface tak transmit karti hain. "
        "Sabse neeche underground area me GOB Zone—yaani collapsed roof void—hydraulic roof support shearer, aur coal pillars dikhaye gaye hain. "
        "Jaise hi underground caving start hoti hai, surface pins aur GOB zone border ka color real-time dynamic update hota hai.\"</i>"
    )
    elements.append(Paragraph(vn_3, voice_style))
    elements.append(Spacer(1, 6))

    vn_4 = (
        "<b>🎙️ Voice Note 4: GIS Satellite Map & Node Mesh Overlay</b><br/>"
        "<i>\"Neeche left side par hamara Surface Panel GIS Map hai jo High-Definition Esri World Imagery Satellite Tiles use karta hai. "
        "Yeh map Jharia Coalfield ke actual GPS coordinates par surface sensor nodes ko pinpoint karta hai. "
        "Node N3 center max-stress zone par positioned hai. Marker par click karne se node ka real-time tilt, strain, vibration, battery, aur TinyML isolation forest status popup me khul jaata hai. "
        "Ground risk ke aadhar par color dots green, yellow, red, ya purple me transform ho jaate hain.\"</i>"
    )
    elements.append(Paragraph(vn_4, voice_style))
    elements.append(Spacer(1, 6))

    vn_5 = (
        "<b>🎙️ Voice Note 5: Gateway Early Warning Status & Blast Filter</b><br/>"
        "<i>\"Bottom right side par hamara Master Gateway Early Warning Status panel hai jo 0.0 se 1.0 ke scale par live subsidence risk score dikhata hai. "
        "Jab underground dynamite blasting hoti hai, toh traditional sensors false alarm trigger kar dete hain aur mining ko faltu me rokna padta hai. "
        "Lekin hamara Stage 2 Gateway Spatial Correlator detect karta hai ki high vibration ke saath TILT 0 hai. "
        "Ise yeh OPERATIONAL BLAST (FILTERED) classify karke physical siren ko suppress kar deta hai, jisse false alarm rukta hai aur mining bina kisi rukaawat ke chalti rehti hai!\"</i>"
    )
    elements.append(Paragraph(vn_5, voice_style))
    elements.append(Spacer(1, 6))

    vn_6 = (
        "<b>🎙️ Voice Note 6: Interactive 3-Tier ML Test Bench & Sliders</b><br/>"
        "<i>\"Ab hum ML Test Bench tab par hain. Yahan Node N3 ke 8 physical sensor sliders—Tilt Mean, Tilt Rate, Strain Delta, Vibration RMS, Peak, Frequency, aur Crack Breakwire—ko live manipulate kar sakte hain. "
        "Right side par hamara 3-Tier ML Model inference result dikhata hai:<br/>"
        "1. Stage 1 Edge TinyML (ESP32-S3) Isolation Forest C model ko 86.4 microseconds me execute karta hai.<br/>"
        "2. Stage 2 Gateway Correlator adjacent nodes ka spatial correlation aur blast suppression evaluate karta hai.<br/>"
        "3. Stage 3 Cloud Multi-Output LSTM (TensorFlow Keras) 24-hour sequence window se surface displacement millimeters me aur severity class predict karta hai.\"</i>"
    )
    elements.append(Paragraph(vn_6, voice_style))
    elements.append(Spacer(1, 6))

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

    # SECTION 3: REMOTE DEPLOYMENT GUIDE IN HINGLISH
    elements.append(Paragraph("3. Remote Deployment Guide in Hinglish (Ghar + On-Site Team)", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    dep_html = (
        "<b>🏠 AAP (Ghar Par - Remote Developer):</b><br/>"
        "1. Github repository <code>https://github.com/Monaal5/mine_subsidence_ml.git</code> par code updated hai.<br/>"
        "2. <b>Render.com</b> par New Web Service banakar GitHub connect karein. Docker select karke Deploy par click karein.<br/>"
        "3. 2 minute me Render aapko public link dega: <code>https://mine-subsidence-app.onrender.com</code>.<br/>"
        "4. Modifies RAM usage under 200MB & dynamic PORT binding fixes free-tier memory issues!<br/><br/>"

        "<b>🔧 HARDWARE TEAM (On-Site Location):</b><br/>"
        "1. <b>ESP32-S3 Sensor Nodes Flashing:</b> ESP32-S3 ko USB se laptop me connect karein. Arduino IDE me <code>esp32_firmware/main.ino</code> kholein. Board <i>ESP32S3 Dev Module</i> aur COM port select karke Upload (Arrow) button dabayein.<br/>"
        "2. <b>Local Gateway Starter:</b> Gateway PC par <code>run_local_gateway.bat</code> ko double click karein. Server 1-click me port 8050 par chalu ho jaayega."
    )
    elements.append(Paragraph(dep_html, body_style))
    elements.append(Spacer(1, 14))

    # Footer banner
    footer_p = ParagraphStyle(
        'FooterP',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        textColor=PRIMARY,
        alignment=TA_CENTER
    )
    elements.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=4, spaceAfter=6))
    elements.append(Paragraph("MineTrac AI Mining Platform © 2026 | Built for Smart India Hackathon (SIH26) Problem Statement", footer_p))

    doc.build(elements)
    print(f"PDF Generated Successfully at: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
