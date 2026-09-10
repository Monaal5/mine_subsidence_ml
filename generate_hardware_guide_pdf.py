"""
Generate MineTrac Hardware Deployment & Cloud Integration Runbook PDF (SIH26)
=============================================================================
Creates a beautifully formatted PDF document detailing the 2-Node ESP32 setup,
ESP-NOW protocol, Master Gateway firmware, Render Cloud integration, and Demo Runbook.
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
    pdf_filename = os.path.join(base_dir, "MineTrac_Hardware_Deployment_Guide_SIH26.pdf")
    
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
    PRIMARY = colors.HexColor("#0f172a")     # Slate 900 / Dark Navy
    SECONDARY = colors.HexColor("#0284c7")   # Sky Blue / Accent
    BRAND_RED = colors.HexColor("#dc2626")   # Alert Red
    BRAND_GREEN = colors.HexColor("#16a34a") # Safe Green
    GOLD = colors.HexColor("#d97706")        # Amber / Gold
    DARK_TEXT = colors.HexColor("#1e293b")   # Dark Slate Text
    MUTED_TEXT = colors.HexColor("#475569")  # Slate Gray
    BG_BOX = colors.HexColor("#f8fafc")      # Box Fill
    BORDER_CLR = colors.HexColor("#cbd5e1")  # Border Gray
    CODE_BG = colors.HexColor("#0f172a")     # Dark Code Fill
    CODE_FG = colors.HexColor("#38bdf8")     # Code Cyan Text

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=PRIMARY,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        alignment=TA_CENTER
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=DARK_TEXT,
        alignment=TA_JUSTIFY,
        spaceBefore=2,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#e2e8f0"),
        alignment=TA_LEFT
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0f172a"),
        alignment=TA_LEFT
    )

    elements = []

    # Title Header Banner
    elements.append(Paragraph("MineTrac AI — Hardware Deployment & Cloud Runbook (SIH26)", title_style))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph("Complete 2-Node ESP32 Setup, ESP-NOW Protocol, Master Gateway & Live Dashboard Integration", subtitle_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=2, spaceAfter=10))

    # Executive Overview Box
    overview_html = (
        "<b>📌 Executive Overview:</b><br/>"
        "This runbook documents the complete end-to-end hardware pipeline for the <b>2-Node ESP32 Hardware Setup</b> "
        "(Slave Node with MPU6050, ADXL345, DS3231 RTC → Master Gateway ESP32 → Render Cloud Dashboard). "
        "It includes resolved TinyML edge inference bug fixes, C header source code, FastAPI live ingestion schemas, "
        "and step-by-step flashing instructions for Rishi and the hardware team."
    )
    elements.append(Paragraph(overview_html, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 1: SYSTEM ARCHITECTURE & DATA FLOW
    elements.append(Paragraph("1. System Architecture & Data Flow", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    arch_html = (
        "<b>Component Overview & Network Hops:</b><br/>"
        "• <b>Slave Node (ESP32 Dev Module):</b> Connects to MPU6050 (<i>0x69</i>), ADXL345 (<i>0x53</i>), and DS3231 RTC. "
        "Calculates tilt angle (pitch & roll), vibration RMS vector magnitude, applies a Stage 1 pre-filter rule "
        "(<i>tilt > 3.5° or vib_rms > 1.8 m/s²</i>), packs the <code>SensorPayload</code> struct, and transmits every 1 second via <b>ESP-NOW</b>.<br/>"
        "• <b>Master Gateway Node (ESP32 Dev Module):</b> Listens for ESP-NOW packets from the Slave Node. "
        "Connects to an Android Phone Hotspot WiFi in STA mode, formats incoming packet data into JSON, and sends an <b>HTTPS POST</b> "
        "request to the deployed cloud endpoint (<code>https://mine-subsidence-ml-2rr5.onrender.com/api/ingest</code>).<br/>"
        "• <b>Render Cloud Dashboard (FastAPI):</b> Stores latest node telemetry in-memory, executes Stage 1 Isolation Forest scoring, "
        "tracks a <b>30-second heartbeat timeout</b> for stale/offline node detection, and updates the Leaflet GIS satellite map automatically."
    )
    elements.append(Paragraph(arch_html, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 2: RESOLVED EDGE INFERENCE CRITICAL BUGS
    elements.append(Paragraph("2. Summary of Resolved Edge Inference Bugs", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    bugs_table_data = [
        [Paragraph("<b>Defect</b>", body_style), Paragraph("<b>Root Cause</b>", body_style), Paragraph("<b>Applied Fix & Verification</b>", body_style)],
        [
            Paragraph("<b>1. Type Truncation</b><br/><code>anomaly_detector.h</code>", body_style),
            Paragraph("<code>subsidence_detector_predict()</code> returns <code>float</code> (-avg_depth, e.g. -4.2). Assigned to <code>int pred_class</code>. Checked <code>pred_class < 0</code>, evaluating unconditionally <code>true</code> for all readings.", body_style),
            Paragraph("Captured return value directly as <code>float score</code>. Updated check to <code>res.anomaly_score < ANOMALY_THRESHOLD</code>.<br/><b>Verified:</b> Correct float evaluation.", body_style)
        ],
        [
            Paragraph("<b>2. Score Domain Mismatch</b><br/><code>train_edge_model.py</code>", body_style),
            Paragraph("<code>ANOMALY_THRESHOLD = -0.6127f</code> calibrated from sklearn <code>score_samples()</code> (range ~[-0.8, -0.3]), but C scorer returned raw path depth (-3.0 to -8.0). Every real reading tripped as anomalous.", body_style),
            Paragraph("Calculated Isolation Forest norm factor <i>c(n) = 10.244771f</i> for <i>MAX_SAMPLES = 256</i>. Updated C header to compute <code>s = -powf(2.0f, -(avg_depth / c(n)))</code>.<br/><b>Verified:</b> FPR 1.06%, Detection 93.6%, AUC 0.9631.", body_style)
        ]
    ]

    bugs_table = Table(bugs_table_data, colWidths=[110, 210, 220])
    bugs_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), BG_BOX),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_CLR),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(bugs_table)
    elements.append(Spacer(1, 10))

    # SECTION 3: SHARED PAYLOAD CONTRACT & FIRMWARE CODE
    elements.append(Paragraph("3. Shared Payload Contract & Firmware Source Code", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=6))

    payload_code = (
        "// esp32_firmware/shared_payload.h\n"
        "#ifndef SHARED_PAYLOAD_H\n"
        "#define SHARED_PAYLOAD_H\n"
        "#include <stdint.h>\n\n"
        "typedef struct __attribute__((packed)) {\n"
        "    uint32_t node_id;             // Node ID (1 to 5)\n"
        "    uint32_t timestamp;           // Unix timestamp from DS3231 RTC\n"
        "    float pitch;                  // Pitch angle in degrees\n"
        "    float roll;                   // Roll angle in degrees\n"
        "    float mpu_vib_rms;            // MPU6050 vibration RMS (m/s²)\n"
        "    float adxl_vib_rms;           // ADXL345 vibration RMS (m/s²)\n"
        "    uint8_t stage1_anomaly_score; // 1 = Alert, 0 = Normal\n"
        "    double lat;                   // Latitude fallback\n"
        "    double lng;                   // Longitude fallback\n"
        "} SensorPayload;\n"
        "#endif // SHARED_PAYLOAD_H"
    )

    t_code1 = Table([[Paragraph(payload_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[540])
    t_code1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR)
    ]))
    elements.append(t_code1)
    elements.append(Spacer(1, 10))

    # Master Gateway Excerpt
    gateway_code = (
        "// esp32_firmware/master_gateway.ino (Snippet)\n"
        "void forwardToDashboard(const SensorPayload &p) {\n"
        "    HTTPClient http;\n"
        "    http.begin(\"https://mine-subsidence-ml-2rr5.onrender.com/api/ingest\");\n"
        "    http.addHeader(\"Content-Type\", \"application/json\");\n"
        "    char jsonPayload[320];\n"
        "    snprintf(jsonPayload, sizeof(jsonPayload),\n"
        "        \"{\\\"node_id\\\":%u,\\\"timestamp\\\":%u,\\\"pitch\\\":%.2f,\\\"roll\\\":%.2f,\"\n"
        "        \"\\\"mpu_vib_rms\\\":%.2f,\\\"adxl_vib_rms\\\":%.2f,\\\"stage1_anomaly_score\\\":%u,\"\n"
        "        \"\\\"lat\\\":%.6f,\\\"lng\\\":%.6f}\",\n"
        "        p.node_id, p.timestamp, p.pitch, p.roll, p.mpu_vib_rms, p.adxl_vib_rms,\n"
        "        p.stage1_anomaly_score, p.lat, p.lng);\n"
        "    int resCode = http.POST(jsonPayload);\n"
        "    Serial.printf(\"[GATEWAY] POST to Dashboard -> Code %d\\n\", resCode);\n"
        "    http.end();\n"
        "}"
    )

    t_code2 = Table([[Paragraph(gateway_code.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)]], colWidths=[540])
    t_code2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('BOX', (0,0), (-1,-1), 1, BORDER_CLR)
    ]))
    elements.append(t_code2)
    elements.append(Spacer(1, 10))

    # PAGE BREAK FOR RUNBOOK & CHECKLIST
    elements.append(PageBreak())

    # SECTION 4: STEP-BY-STEP HARDWARE FLASHING RUNBOOK
    elements.append(Paragraph("4. Step-by-Step Hardware Flashing & Demo Runbook", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    runbook_steps = (
        "<b>Step 1: Flash Master Gateway First & Get MAC Address</b><br/>"
        "1. Open <code>esp32_firmware/master_gateway.ino</code> in Arduino IDE.<br/>"
        "2. Update the phone hotspot credentials:<br/>"
        "   <code>const char* WIFI_SSID = \"YOUR_PHONE_HOTSPOT_SSID\";</code><br/>"
        "   <code>const char* WIFI_PASSWORD = \"YOUR_HOTSPOT_PASSWORD\";</code><br/>"
        "3. Flash the Master ESP32. Open Serial Monitor at <b>115200 baud</b>.<br/>"
        "4. Copy the printed MAC address from boot logs, e.g.:<br/>"
        "   <code>[CRITICAL] Master MAC Address: 24:0A:C4:XX:XX:XX</code><br/><br/>"

        "<b>Step 2: Flash Slave Node</b><br/>"
        "1. Open <code>esp32_firmware/slave_node.ino</code> in Arduino IDE.<br/>"
        "2. Set hotspot credentials and paste the Master MAC address into <code>masterAddress[]</code>:<br/>"
        "   <code>uint8_t masterAddress[] = {0x24, 0x0A, 0xC4, 0xXX, 0xXX, 0xXX};</code><br/>"
        "3. Connect MPU6050 (AD0 to 3.3V → <i>0x69</i>), ADXL345 (<i>0x53</i>), and DS3231 RTC.<br/>"
        "4. Flash the Slave ESP32.<br/><br/>"

        "<b>Step 3: Venue Demo Readiness & Pre-Warming Checklist</b><br/>"
        "1. Enable Android Phone Hotspot (ensure 2.4GHz band is active).<br/>"
        "2. Power on both Slave and Master ESP32 modules.<br/>"
        "3. <b>1 Minute Before Demo:</b> Open <code>https://mine-subsidence-ml-2rr5.onrender.com/api/health</code> in browser "
        "to pre-warm the Render free-tier container and avoid cold-start delay.<br/>"
        "4. Open the main live dashboard: <code>https://mine-subsidence-ml-2rr5.onrender.com/</code>.<br/>"
        "5. <b>Live Action:</b> Tilt the Slave sensor (> 3.5°) or apply vibration (> 1.8 m/s²). "
        "The node marker on the GIS map turns <b>RED</b> (<code>ALERT / ANOMALY</code>) in real time!"
    )
    elements.append(Paragraph(runbook_steps, body_style))
    elements.append(Spacer(1, 10))

    # SECTION 5: TROUBLESHOOTING & CONTINGENCY PLAN
    elements.append(Paragraph("5. Troubleshooting & Contingency Plan", h1_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=BORDER_CLR, spaceBefore=2, spaceAfter=8))

    trouble_html = (
        "• <b>Issue: ESP-NOW Packets Not Arriving at Master</b><br/>"
        "  <i>Cause:</i> MAC address mismatch or WiFi channel drift.<br/>"
        "  <i>Fix:</i> Ensure Slave connects to phone hotspot at boot to auto-sync its WiFi channel with the Master, and verify `masterAddress[]` matches byte-for-byte.<br/><br/>"
        "• <b>Issue: Render Dashboard Shows 404 / Slow Response</b><br/>"
        "  <i>Cause:</i> Free-tier container idling after 15 minutes of inactivity.<br/>"
        "  <i>Fix:</i> Hit <code>/api/health</code> 60 seconds before your presentation slot.<br/><br/>"
        "• <b>Issue: Master HTTP POST Fails (Connection Error)</b><br/>"
        "  <i>Cause:</i> Phone hotspot lacks cellular data internet connectivity.<br/>"
        "  <i>Fix:</i> Verify phone has mobile data enabled, or switch to laptop local server (<code>http://<laptop-ip>:8050/api/ingest</code>)."
    )
    elements.append(Paragraph(trouble_html, body_style))
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
    elements.append(Paragraph("MineTrac Hardware Integration Guide © 2026 | Built for Smart India Hackathon (SIH26)", footer_p))

    doc.build(elements)
    print(f"PDF Generated Successfully at: {pdf_filename}")

if __name__ == "__main__":
    generate_pdf()
