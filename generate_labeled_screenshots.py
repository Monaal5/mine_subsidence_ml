"""
Labeled Diagram Generator — Creates High-Resolution Annotated Visual Screenshots for MineTrac Dashboard
================================================================================-------------------------
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

viz_dir = r"d:\innertask\mine_subsidence_ml\visualization"
os.makedirs(viz_dir, exist_ok=True)

# -----------------------------------------------------------------------------
# DIAGRAM 1: TAB 1 — LIVE ENTERPRISE DASHBOARD & MINE CUTAWAY (LABELED)
# -----------------------------------------------------------------------------
def generate_tab1_labeled():
    fig, ax = plt.subplots(figsize=(14, 11), dpi=150)
    fig.patch.set_facecolor('#f1f5f9')
    ax.set_facecolor('#f1f5f9')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 97.5, "MineTrac AI — Live Enterprise Dashboard & Mine Cutaway (Labeled UI Diagram)",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    # Top Header Box
    rect_top = patches.FancyBboxPatch((2, 88), 96, 7.5, boxstyle="round,pad=0.3",
                                      ec="#cbd5e1", fc="#ffffff", lw=1.5)
    ax.add_patch(rect_top)
    ax.text(4, 93, "M  MineTrac AI  by AKSSAI ProjExcel", fontsize=11, fontweight='bold', color='#e11d48')
    ax.text(40, 93, "[📋 Reports]  [👥 All Nodes]  [🛡️ Safety Rules]  [⚙️ Master Config]", fontsize=9, fontweight='bold', color='#0284c7')
    ax.text(78, 93, "[🔇 Audio Siren: MUTED]", fontsize=9, fontweight='bold', color='#dc2626', bbox=dict(boxstyle="round", fc="#ffe4e6", ec="#fecdd3"))
    ax.text(92, 93, "👤 Justin H.", fontsize=9, fontweight='bold', color='#0f172a')

    # Secondary Tabs
    rect_tabs = patches.FancyBboxPatch((2, 82), 96, 4.5, boxstyle="round,pad=0.2", ec="#cbd5e1", fc="#ffffff", lw=1)
    ax.add_patch(rect_tabs)
    ax.text(5, 84, "Dashboard [ACTIVE (Red Line)]", fontsize=9, fontweight='bold', color='#e11d48')
    ax.text(25, 84, "ML Test Bench (3-Tier)", fontsize=9, color='#64748b')
    ax.text(48, 84, "90-Day Simulation", fontsize=9, color='#64748b')
    ax.text(70, 84, "Hardware Guide", fontsize=9, color='#64748b')

    # Metric Summary Cards Row
    for i, (title, val, sub, col, bg_col) in enumerate([
        ("Active Mesh Nodes", "5 / 5 Online", "100% Signal", "#16a34a", "#dcfce7"),
        ("Max Surface Tilt", "0.02°", "Normal Baseline", "#d97706", "#fef3c7"),
        ("Max Strain Stress Delta", "0.5 µε", "Tensile Normal", "#0284c7", "#e0f2fe"),
        ("Subsidence Risk %", "2.4%", "SAFE_STABLE", "#dc2626", "#fee2e2")
    ]):
        x = 2 + i * 24.2
        r = patches.FancyBboxPatch((x, 71), 23.2, 9, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1)
        ax.add_patch(r)
        ax.text(x+2, 77.5, title, fontsize=8, color='#64748b', fontweight='bold')
        ax.text(x+2, 74.5, val, fontsize=12, color='#0f172a', fontweight='bold')
        ax.text(x+2, 72.2, sub, fontsize=7.5, color=col, fontweight='bold')

    # Preset Test Chips
    rect_presets = patches.FancyBboxPatch((2, 64), 96, 5, boxstyle="round,pad=0.2", ec="#e2e8f0", fc="#ffffff", lw=1)
    ax.add_patch(rect_presets)
    ax.text(3, 66.2, "🧪 Test Scenarios:", fontsize=8.5, fontweight='bold', color='#e11d48')
    ax.text(18, 66.2, "[Case 1: Normal]", fontsize=8, color='#15803d', bbox=dict(boxstyle="round", fc="#dcfce7", ec="#86efac"))
    ax.text(34, 66.2, "[Case 2: Pre-Subsidence]", fontsize=8, color='#b45309', bbox=dict(boxstyle="round", fc="#fef3c7", ec="#fde047"))
    ax.text(54, 66.2, "[Case 3: Active Siren!]", fontsize=8, color='#b91c1c', bbox=dict(boxstyle="round", fc="#fee2e2", ec="#fca5a5"))
    ax.text(73, 66.2, "[Case 4: Blast]", fontsize=8, color='#6b21a8', bbox=dict(boxstyle="round", fc="#f3e8ff", ec="#d8b4fe"))
    ax.text(86, 66.2, "[Case 5: Trip]", fontsize=8, color='#c2410c', bbox=dict(boxstyle="round", fc="#ffedd5", ec="#fdba74"))

    # Mine Cutaway Schematic
    rect_schematic = patches.FancyBboxPatch((2, 33), 96, 29, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(rect_schematic)
    ax.text(4, 59, "🏗️ Underground Longwall Mine Cross-Section & Sensor Mesh Overlay", fontsize=10, fontweight='bold', color='#0f172a')
    
    # Surface Facilities Sub-box
    rect_surf = patches.Rectangle((4, 49), 92, 8, ec="#cbd5e1", fc="#e2e8f0", lw=1)
    ax.add_patch(rect_surf)
    ax.text(6, 54, "🏭 Preparation Plant    🛢️ Raw-Coal Silo    🛗 Shaft Head", fontsize=8.5, fontweight='bold', color='#1e293b')
    ax.text(6, 50.5, "Surface Panel Track: (Slave N1)----(Slave N2)----(Slave N3 Center-Max)----(Slave N4)----(Slave N5)", fontsize=8, fontweight='bold', color='#0284c7')

    # Underground Strata Sub-box
    rect_under = patches.Rectangle((4, 35), 92, 12, ec="#cbd5e1", fc="#f8fafc", lw=1)
    ax.add_patch(rect_under)
    ax.text(5, 44, "Overburden Sandstone & Shale Strata Layers (Transmits Caving Strain Upward)", fontsize=8, fontweight='bold', color='#3730a3', bbox=dict(boxstyle="square", fc="#e0e7ff", ec="#a5b4fc"))
    ax.text(5, 40, "🛗 Elevator Shaft    |  GOB ZONE (Collapsed Roof Void)  |  ⚙️ Longwall Shearer  |  🚜 Continuous Miner", fontsize=8, fontweight='bold', color='#0f172a')
    ax.text(5, 36.5, "Haulage Slope ➔     |  [High Deformation Risk Area]   |  [Hydraulic Supports] |  [Pillars: Block, Block]", fontsize=7.5, color='#64748b')

    # GIS Map & Gateway Risk Gauge
    rect_map = patches.FancyBboxPatch((2, 2), 60, 29, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1)
    ax.add_patch(rect_map)
    ax.text(4, 28, "🗺️ Surface Panel GIS Coordinates (Leaflet OpenStreetMap)", fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(4, 15, "GPS Coordinates: Jharia Panel [23.795, 86.431]\nMarkers N1-N5: Green=Normal, Yellow=Creep, Red=Collapse, Purple=Blast", fontsize=8, color='#64748b')

    rect_alert = patches.FancyBboxPatch((64, 2), 34, 29, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1)
    ax.add_patch(rect_alert)
    ax.text(66, 28, "🚨 Gateway Early Warning Status", fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(78, 21, "0.02", fontsize=22, fontweight='bold', color='#16a34a', ha='center')
    ax.text(78, 18, "Risk Score (0.0 to 1.0)", fontsize=7.5, color='#64748b', ha='center')
    ax.text(66, 12, "🟢 NORMAL_STABLE\nAll surface mesh nodes safe.", fontsize=8, color='#15803d', bbox=dict(boxstyle="round", fc="#dcfce7", ec="#86efac"))
    ax.text(66, 5, "Max Tilt: 0.02°  |  Strain: 0.5 µε\nEst. Disp: 0.0 mm | Siren: MUTED", fontsize=7.5, color='#475569')

    # CALLOUT ARROWS & LABELS
    ax.annotate("Line 1: Top Navigation Modals", xy=(42, 93), xytext=(42, 98),
                arrowprops=dict(arrowstyle="->", color="#e11d48", lw=1.5), fontsize=8, fontweight='bold', color="#e11d48")
    
    ax.annotate("Line 2: Audio Siren Toggle Button", xy=(78, 93), xytext=(70, 98),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5), fontsize=8, fontweight='bold', color="#dc2626")

    ax.annotate("Line 3: Secondary Red Underline Tabs", xy=(15, 84), xytext=(5, 88.5),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, fontweight='bold', color="#0284c7")

    ax.annotate("Line 4: MineTrac Metric Summary Cards", xy=(50, 75), xytext=(40, 81),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.5), fontsize=8, fontweight='bold', color="#16a34a")

    ax.annotate("Line 5: Test Case Scenario Chips", xy=(40, 66.2), xytext=(40, 61),
                arrowprops=dict(arrowstyle="->", color="#9333ea", lw=1.5), fontsize=8, fontweight='bold', color="#9333ea")

    ax.annotate("Line 6: Surface Facility Overlay", xy=(25, 54), xytext=(25, 60),
                arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.5), fontsize=8, fontweight='bold', color="#0f172a")

    ax.annotate("Line 7: Surface Sensor Mesh Pins (N1-N5)", xy=(50, 50.5), xytext=(50, 46),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, fontweight='bold', color="#0284c7")

    ax.annotate("Line 8: Underground Gob Collapse Void", xy=(40, 40), xytext=(40, 31),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5), fontsize=8, fontweight='bold', color="#dc2626")

    ax.annotate("Line 9: GIS Leaflet OpenStreetMap Grid", xy=(30, 15), xytext=(30, 31),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, fontweight='bold', color="#0284c7")

    ax.annotate("Line 10: Gateway Early Warning Meter", xy=(80, 18), xytext=(75, 31),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.5), fontsize=8, fontweight='bold', color="#16a34a")

    plt.tight_layout()
    out_path = os.path.join(viz_dir, "dashboard_tab1_labeled.png")
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# DIAGRAM 2: TAB 2 — ML TEST BENCH (SLIDERS & 3-TIER INFERENCE)
# -----------------------------------------------------------------------------
def generate_tab2_labeled():
    fig, ax = plt.subplots(figsize=(14, 10), dpi=150)
    fig.patch.set_facecolor('#f1f5f9')
    ax.set_facecolor('#f1f5f9')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 97, "MineTrac AI — ML Test Bench & 3-Tier Model Inference (Labeled Diagram)",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    # Left Column: Sensor Input Sliders Panel
    rect_left = patches.FancyBboxPatch((2, 5), 46, 88, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(rect_left)
    ax.text(4, 89, "🎛️ Sensor Input Parameters (Node N3 - Center)", fontsize=11, fontweight='bold', color='#0f172a')
    ax.text(4, 85, "Presets: [Normal]  [Pre-Subsidence]  [Active]  [Blast]", fontsize=8.5, fontweight='bold', color='#0284c7')

    sliders = [
        ("Tilt Mean (°)", "0.02°"), ("Tilt Rate (°/min)", "0.0001°"),
        ("Strain Delta (µε)", "0.5 µε"), ("Vibration RMS (g)", "0.025g"),
        ("Vibration Peak (g)", "0.06g"), ("Dominant Freq (Hz)", "14.5 Hz"),
        ("Crack Breakwire", "1 - Intact"), ("Temp-Humidity Index", "0.55")
    ]
    for i, (s_name, s_val) in enumerate(sliders):
        y = 77 - i * 9
        rect_s = patches.Rectangle((4, y), 42, 6.5, ec="#cbd5e1", fc="#f8fafc", lw=1)
        ax.add_patch(rect_s)
        ax.text(6, y+4, s_name, fontsize=8, fontweight='bold', color='#475569')
        ax.text(32, y+4, s_val, fontsize=8, fontweight='bold', color='#0284c7')
        # Draw fake slider line
        ax.plot([6, 42], [y+1.8, y+1.8], color="#cbd5e1", lw=3)
        ax.plot([6, 12], [y+1.8, y+1.8], color="#0284c7", lw=3)
        ax.plot([12], [y+1.8], marker='o', markersize=6, color="#0284c7")

    # Right Column: 3-Tier ML Model Inference Results Panel
    rect_right = patches.FancyBboxPatch((52, 5), 46, 88, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(rect_right)
    ax.text(54, 89, "🤖 Three-Tier ML Model Inference Results", fontsize=11, fontweight='bold', color='#0f172a')

    # Stage 1 Card
    r_st1 = patches.FancyBboxPatch((54, 60), 42, 26, boxstyle="round,pad=0.2", ec="#cbd5e1", fc="#f8fafc", lw=1)
    ax.add_patch(r_st1)
    ax.text(56, 82, "Stage 1: Slave Node Edge TinyML (ESP32-S3)", fontsize=9, fontweight='bold', color='#0f172a')
    ax.text(56, 78, "C Header: isolation_forest_model.h (49.3 KB)", fontsize=7.5, color='#0284c7', fontweight='bold')
    ax.text(56, 73, "Anomaly Rating:  NORMAL", fontsize=8.5, fontweight='bold', color='#16a34a')
    ax.text(56, 68, "Raw Anomaly Score: -0.4720  (Threshold: -0.6127)", fontsize=8, color='#475569')
    ax.text(56, 63, "ESP32 Execution Speed: 112.4 µs (< 150 µs target)", fontsize=8, fontweight='bold', color='#16a34a')

    # Stage 2 Card
    r_st2 = patches.FancyBboxPatch((54, 33), 42, 24, boxstyle="round,pad=0.2", ec="#cbd5e1", fc="#f8fafc", lw=1)
    ax.add_patch(r_st2)
    ax.text(56, 53, "Stage 2: Master Node Gateway Correlator", fontsize=9, fontweight='bold', color='#0f172a')
    ax.text(56, 49, "Offline Rules Engine (Spatial Correlation)", fontsize=7.5, color='#0284c7', fontweight='bold')
    ax.text(56, 44, "Evaluated Event Type: NORMAL_STABLE", fontsize=8.5, fontweight='bold', color='#16a34a')
    ax.text(56, 39, "Blast Filter Action: No Blast Filtered", fontsize=8, color='#475569')
    ax.text(56, 35, "Physical Siren & SMS: Muted / Safe", fontsize=8, color='#475569')

    # Stage 3 Card
    r_st3 = patches.FancyBboxPatch((54, 6), 42, 24, boxstyle="round,pad=0.2", ec="#cbd5e1", fc="#f8fafc", lw=1)
    ax.add_patch(r_st3)
    ax.text(56, 26, "Stage 3: Cloud LSTM Spatial-Temporal Predictor", fontsize=9, fontweight='bold', color='#0f172a')
    ax.text(56, 22, "TensorFlow Keras (24-Hour Lookback Window)", fontsize=7.5, color='#0284c7', fontweight='bold')
    ax.text(56, 17, "Subsidence Risk Probability: 2.4%", fontsize=8.5, fontweight='bold', color='#16a34a')
    ax.text(56, 12, "Predicted Max Displacement: 0.8 mm (MAE: 7.26mm)", fontsize=8, color='#475569')
    ax.text(56, 8, "Predicted Severity Class: LOW", fontsize=8.5, fontweight='bold', color='#16a34a')

    # Annotations
    ax.annotate("Line 1: Preset Buttons", xy=(25, 85), xytext=(25, 93),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, fontweight='bold', color="#0284c7")

    ax.annotate("Line 2: Live Sensor Sliders", xy=(25, 55), xytext=(2, 55),
                arrowprops=dict(arrowstyle="->", color="#e11d48", lw=1.5), fontsize=8, fontweight='bold', color="#e11d48")

    ax.annotate("Line 3: Stage 1 TinyML Output", xy=(75, 73), xytext=(85, 73),
                arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.5), fontsize=8, fontweight='bold', color="#16a34a")

    ax.annotate("Line 4: Stage 2 Gateway Correlator", xy=(75, 44), xytext=(85, 44),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, fontweight='bold', color="#0284c7")

    ax.annotate("Line 5: Stage 3 Cloud LSTM Predictor", xy=(75, 17), xytext=(85, 17),
                arrowprops=dict(arrowstyle="->", color="#9333ea", lw=1.5), fontsize=8, fontweight='bold', color="#9333ea")

    plt.tight_layout()
    out_path = os.path.join(viz_dir, "dashboard_tab2_labeled.png")
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# -----------------------------------------------------------------------------
# DIAGRAM 3: TAB 3 — 90-DAY SIMULATION PLAYER & MODALS (LABELED)
# -----------------------------------------------------------------------------
def generate_tab3_and_modals_labeled():
    # Tab 3 Player
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('#f1f5f9')
    ax.set_facecolor('#f1f5f9')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "MineTrac AI — 90-Day Simulation Player & Timeline (Labeled Diagram)",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    # 4 Scenario Buttons
    for i, (phase, icon, col, bg_col, desc) in enumerate([
        ("Phase 1: Normal (Days 0-60)", "🟢", "#15803d", "#dcfce7", "Stable baseline noise & thermal drift"),
        ("Phase 2: Pre-Subsidence (60-75)", "🟡", "#b45309", "#fef3c7", "Monotonic tilt ramp 0.05° -> 0.3°"),
        ("Phase 3: Active Collapse (75-85)", "🔴", "#b91c1c", "#fee2e2", "Accelerating tilt >1.5°, breakwire flip"),
        ("Phase 4: Dynamite Blast", "🟣", "#6b21a8", "#f3e8ff", "Vibration 1.2g spike with ZERO tilt creep")
    ]):
        x = 2 + i * 24.2
        r = patches.FancyBboxPatch((x, 75), 23.2, 16, boxstyle="round,pad=0.3", ec=col, fc=bg_col, lw=1.5)
        ax.add_patch(r)
        ax.text(x+2, 87, f"{icon} {phase}", fontsize=8.5, fontweight='bold', color=col)
        ax.text(x+2, 78, desc, fontsize=7.5, color='#475569')

    # Large Timeline Chart Box
    rect_chart = patches.FancyBboxPatch((2, 5), 96, 65, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(rect_chart)
    ax.text(4, 65, "📈 Multi-Sensor Telemetry Streams Across 90-Day Lifecycle Window", fontsize=11, fontweight='bold', color='#0f172a')
    
    # Fake chart curves
    x_pts = np.linspace(5, 95, 100)
    y_tilt = 12 + (x_pts > 60) * ((x_pts - 60)**1.4) * 0.4
    y_strain = 10 + (x_pts > 60) * ((x_pts - 60)**1.2) * 0.3
    
    ax.plot(x_pts, y_tilt, color="#dc2626", lw=2, label="Center Node N3 Tilt (°)")
    ax.plot(x_pts, y_strain, color="#d97706", lw=2, label="Center Node N3 Strain (µε)")
    ax.legend(loc="upper left")

    ax.annotate("Line 1: Phase Scenario Buttons", xy=(35, 83), xytext=(35, 94),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.5), fontsize=8, fontweight='bold', color="#0284c7")

    ax.annotate("Line 2: Pre-Subsidence Onset (Day 60)", xy=(60, 20), xytext=(45, 35),
                arrowprops=dict(arrowstyle="->", color="#d97706", lw=1.5), fontsize=8, fontweight='bold', color="#d97706")

    ax.annotate("Line 3: Active Collapse Trough (Day 75+)", xy=(85, 45), xytext=(70, 55),
                arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.5), fontsize=8, fontweight='bold', color="#dc2626")

    plt.tight_layout()
    out_path = os.path.join(viz_dir, "dashboard_tab3_labeled.png")
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

    # Modals Labeled Diagram
    fig, ax = plt.subplots(figsize=(14, 8), dpi=150)
    fig.patch.set_facecolor('#f1f5f9')
    ax.set_facecolor('#f1f5f9')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    ax.text(50, 96, "MineTrac AI — Interactive Popups & Modals (Labeled Diagram)",
            fontsize=15, fontweight='bold', ha='center', color='#0f172a')

    # Modal 1: Reports
    r_m1 = patches.FancyBboxPatch((2, 52), 46, 40, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(r_m1)
    ax.text(4, 87, "📋 Mining Safety & Subsidence Daily Report Modal", fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(4, 83, "Parameter | Target Limit | Current Reading | Status", fontsize=8, fontweight='bold', color='#0284c7')
    ax.text(4, 78, "Max Surface Tilt   | < 0.50° | 0.02° | 🟢 Normal\nStrain Stress Delta | < 15.0uE| 0.5 uE | 🟢 Normal\nVibration RMS      | < 0.10g | 0.025g| 🟢 Normal\nBreakwire State    | 1 Intact| 1     | 🟢 Normal", fontsize=7.5, color='#475569')

    # Modal 2: All Nodes Grid
    r_m2 = patches.FancyBboxPatch((52, 52), 46, 40, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(r_m2)
    ax.text(54, 87, "👥 Surface Panel Mesh Nodes Grid (N1-N5) Modal", fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(54, 83, "Node | Zone | Tilt | Strain | Battery | Rating", fontsize=8, fontweight='bold', color='#0284c7')
    ax.text(54, 78, "N1 | Edge Panel | 0.01° | 0.2uE | 98% Solar | 🟢 NORMAL\nN2 | Mid Panel  | 0.02° | 0.4uE | 95% Solar | 🟢 NORMAL\nN3 | Center Max | 0.02° | 0.5uE | 99% Solar | 🟢 NORMAL\nN4 | Mid Panel  | 0.02° | 0.3uE | 96% Solar | 🟢 NORMAL\nN5 | Edge Panel | 0.01° | 0.1uE | 97% Solar | 🟢 NORMAL", fontsize=7.5, color='#475569')

    # Modal 3: Safety Rules
    r_m3 = patches.FancyBboxPatch((2, 5), 46, 42, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(r_m3)
    ax.text(4, 42, "🛡️ DGMS Mining Safety Rulebook & Thresholds Modal", fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(4, 36, "Rule 1 (Pre-Subsidence): If tilt > 0.10° or strain > 5.0uE,\nissue Pre-Subsidence Warning to control room.", fontsize=7.5, color='#475569')
    ax.text(4, 26, "Rule 2 (Critical Siren): If tilt > 1.00° or breakwire snaps (0),\ntrigger physical 95dB siren relay & evacuate panel.", fontsize=7.5, color='#dc2626', fontweight='bold')
    ax.text(4, 16, "Rule 3 (Blast Filter): If vibration > 0.5g occurs across\nALL 5 nodes without tilt shift -> Suppress siren.", fontsize=7.5, color='#6b21a8')

    # Modal 4: Master Config
    r_m4 = patches.FancyBboxPatch((52, 5), 46, 42, boxstyle="round,pad=0.3", ec="#e2e8f0", fc="#ffffff", lw=1.5)
    ax.add_patch(r_m4)
    ax.text(54, 42, "⚙️ Master Gateway Node Configuration Modal", fontsize=9.5, fontweight='bold', color='#0f172a')
    ax.text(54, 36, "Sampling Interval: 5 Minutes (300s)\nRadio Frequency: 2.4 GHz ESP-NOW Mesh (Ch 11)\nCellular Uplink: SIM7000 4G LTE (Connected)\nOffline Storage: SQLite (30 Days Capacity)", fontsize=7.5, color='#475569')
    ax.text(54, 16, "[🔊 Test Siren Sound Button] -> Triggers Gateway Relay Test", fontsize=8, fontweight='bold', color='#e11d48', bbox=dict(boxstyle="round", fc="#ffe4e6", ec="#fecdd3"))

    plt.tight_layout()
    out_path_m = os.path.join(viz_dir, "dashboard_modals_labeled.png")
    plt.savefig(out_path_m, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path_m}")

if __name__ == "__main__":
    generate_tab1_labeled()
    generate_tab2_labeled()
    generate_tab3_and_modals_labeled()
