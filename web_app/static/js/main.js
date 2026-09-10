/**
 * MineTrac Official Light Theme Dashboard & Interactive Modals (SIH26)
 * Single Page Application JavaScript Logic
 */

let audioCtx = null;
let sirenOscillator = null;
let sirenGain = null;
let sirenInterval = null;
let isAudioMuted = true;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initModals();
    initSirenAudio();
    initGISMap();
    initLiveChart();
    initMLTestBench();
    initScenarioPlayer();
    initScenarioChart();
    initDashboardPresets();
});

// ============================================================================
// MODALS INTERACTIVITY
// ============================================================================

function initModals() {
    const modalMap = {
        'nav-btn-reports': 'modal-reports',
        'nav-btn-nodes': 'modal-nodes',
        'nav-btn-safety': 'modal-safety',
        'nav-btn-config': 'modal-config'
    };

    Object.keys(modalMap).forEach(btnId => {
        const btn = document.getElementById(btnId);
        const modalId = modalMap[btnId];
        if (btn) {
            btn.addEventListener('click', () => {
                const modal = document.getElementById(modalId);
                if (modal) modal.classList.add('active');
            });
        }
    });

    // Close buttons
    document.querySelectorAll('.modal-close-btn').forEach(closeBtn => {
        closeBtn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal-overlay');
            if (modal) modal.classList.remove('active');
        });
    });

    // Overlay click close
    document.querySelectorAll('.modal-overlay').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) modal.classList.remove('active');
        });
    });

    // Test Siren Trigger in Modal
    const testSirenBtn = document.getElementById('test-siren-trigger');
    if (testSirenBtn) {
        testSirenBtn.addEventListener('click', () => {
            if (!audioCtx) {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                audioCtx = new AudioContext();
            }
            playTestBeep();
            alert("🔊 Gateway High-Decibel Siren Relay Test Triggered!");
        });
    }
}

// ============================================================================
// WEB AUDIO API EMERGENCY SIREN SYNTHESIZER
// ============================================================================

function initSirenAudio() {
    const toggleBtn = document.getElementById('btn-siren-toggle');
    const sirenText = document.getElementById('siren-btn-text');
    const sirenIcon = document.getElementById('siren-icon');

    if (!toggleBtn) return;

    toggleBtn.addEventListener('click', () => {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
        }

        isAudioMuted = !isAudioMuted;

        if (isAudioMuted) {
            toggleBtn.className = 'siren-toggle-btn muted';
            sirenText.textContent = 'Audio Siren: MUTED';
            sirenIcon.textContent = '🔇';
            stopSirenSound();
        } else {
            toggleBtn.className = 'siren-toggle-btn active-siren';
            sirenText.textContent = 'Audio Siren: ACTIVE';
            sirenIcon.textContent = '🔊';
            playTestBeep();
        }
    });
}

function playTestBeep() {
    if (!audioCtx) return;
    try {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + 0.15);
    } catch (e) { console.error(e); }
}

function startSirenSound() {
    if (isAudioMuted || sirenOscillator) return;
    try {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
        }

        sirenOscillator = audioCtx.createOscillator();
        sirenGain = audioCtx.createGain();

        sirenOscillator.type = 'sawtooth';
        sirenOscillator.frequency.setValueAtTime(700, audioCtx.currentTime);
        sirenGain.gain.setValueAtTime(0.15, audioCtx.currentTime);

        sirenOscillator.connect(sirenGain);
        sirenGain.connect(audioCtx.destination);
        sirenOscillator.start();

        let highTone = true;
        sirenInterval = setInterval(() => {
            if (sirenOscillator && audioCtx) {
                const targetFreq = highTone ? 1200 : 700;
                sirenOscillator.frequency.exponentialRampToValueAtTime(targetFreq, audioCtx.currentTime + 0.3);
                highTone = !highTone;
            }
        }, 350);

    } catch (e) {
        console.error("Audio Siren Error:", e);
    }
}

function stopSirenSound() {
    if (sirenInterval) {
        clearInterval(sirenInterval);
        sirenInterval = null;
    }
    if (sirenOscillator) {
        try {
            sirenOscillator.stop();
            sirenOscillator.disconnect();
        } catch (e) {}
        sirenOscillator = null;
    }
}

// ============================================================================
// NAVIGATION TABS
// ============================================================================

function initNavigation() {
    const tabs = document.querySelectorAll('.sec-tab-btn');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const targetId = `tab-${tab.dataset.tab}`;
            const targetContent = document.getElementById(targetId);
            if (targetContent) {
                targetContent.classList.add('active');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
        });
    });
}

// ============================================================================
// GIS MAP PANEL (LEAFLET OPENSTREETMAP INTEGRATION)
// ============================================================================

let map;
let nodeMarkers = {};

const NODE_COORDS = {
    'N1': [23.792, 86.425],
    'N2': [23.794, 86.429],
    'N3': [23.795, 86.431], // Center node
    'N4': [23.796, 86.433],
    'N5': [23.798, 86.437]
};

function initGISMap() {
    map = L.map('gis-map').setView([23.795, 86.431], 15);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap | MineTrac SIH26 Mesh'
    }).addTo(map);

    Object.keys(NODE_COORDS).forEach(nodeId => {
        const coords = NODE_COORDS[nodeId];
        const isCenter = nodeId === 'N3';
        
        const marker = L.circleMarker(coords, {
            radius: isCenter ? 12 : 8,
            fillColor: "#16a34a",
            color: "#ffffff",
            weight: 2,
            opacity: 1,
            fillOpacity: 0.9
        }).addTo(map);

        marker.bindPopup(`
            <div style="color: #0f172a; font-family: sans-serif;">
                <strong>Node ${nodeId} (${isCenter ? 'Center - Max Stress' : 'Mesh Node'})</strong><br>
                Radio: 802.15.4 Mesh Active<br>
                TinyML: Isolation Forest C Header
            </div>
        `);

        nodeMarkers[nodeId] = marker;
    });
}

function updateNodeMapColors(statusMap) {
    const colorMap = {
        'normal': '#16a34a',
        'warning': '#d97706',
        'critical': '#dc2626',
        'blast': '#9333ea'
    };

    Object.keys(statusMap).forEach(nodeId => {
        if (nodeMarkers[nodeId]) {
            const color = colorMap[statusMap[nodeId]] || '#16a34a';
            nodeMarkers[nodeId].setStyle({ fillColor: color });
        }
    });

    const pinN3 = document.getElementById('pin-n3');
    const gobZone = document.getElementById('gob-zone');
    if (pinN3 && statusMap['N3']) {
        const status = statusMap['N3'];
        if (status === 'critical') {
            pinN3.style.borderColor = '#dc2626';
            gobZone.style.borderColor = '#dc2626';
            gobZone.style.background = '#fee2e2';
        } else if (status === 'warning') {
            pinN3.style.borderColor = '#d97706';
            gobZone.style.borderColor = '#d97706';
            gobZone.style.background = '#fef3c7';
        } else {
            pinN3.style.borderColor = '#16a34a';
            gobZone.style.borderColor = '#dc2626';
            gobZone.style.background = '#fee2e2';
        }
    }
}

// ============================================================================
// LIVE TELEMETRY CHART (Light Theme)
// ============================================================================

let liveChart;

function initLiveChart() {
    const canvas = document.getElementById('liveChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const labels = Array.from({length: 30}, (_, i) => `${i*5}m`);

    liveChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'N3 Center Tilt (°)',
                    borderColor: '#dc2626',
                    backgroundColor: 'rgba(220, 38, 38, 0.08)',
                    data: Array(30).fill(0.02),
                    tension: 0.3,
                    fill: true
                },
                {
                    label: 'N1 Edge Tilt (°)',
                    borderColor: '#0284c7',
                    backgroundColor: 'rgba(2, 132, 199, 0.08)',
                    data: Array(30).fill(0.01),
                    tension: 0.3,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#1e293b', font: { weight: '600' } } } },
            scales: {
                x: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#64748b' } },
                y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#64748b' } }
            }
        }
    });
}

// ============================================================================
// DASHBOARD PRESETS
// ============================================================================

function initDashboardPresets() {
    const p1 = document.getElementById('db-preset-1');
    const p2 = document.getElementById('db-preset-2');
    const p3 = document.getElementById('db-preset-3');
    const p4 = document.getElementById('db-preset-4');
    const p5 = document.getElementById('db-preset-5');

    if (p1) p1.addEventListener('click', () => setPreset(0.02, 0.0001, 0.5, 0.025, 0.06, 14.5, 1));
    if (p2) p2.addEventListener('click', () => setPreset(0.25, 0.008, 8.5, 0.045, 0.12, 10.2, 1));
    if (p3) p3.addEventListener('click', () => setPreset(1.45, 0.035, 32.0, 0.18, 0.65, 4.5, 0));
    if (p4) p4.addEventListener('click', () => setPreset(0.02, 0.0001, 0.5, 0.85, 2.1, 45.0, 1));
    if (p5) p5.addEventListener('click', () => setPreset(0.02, 0.0001, 0.5, 0.025, 0.06, 14.5, 0));
}

// ============================================================================
// ML TEST BENCH & INFERENCE
// ============================================================================

function initMLTestBench() {
    const inputs = ['tilt', 'tilt-rate', 'strain', 'vib-rms', 'vib-peak', 'vib-freq', 'env'];
    
    inputs.forEach(id => {
        const slider = document.getElementById(`input-${id}`);
        const label = document.getElementById(`lbl-${id}`);
        if (slider && label) {
            slider.addEventListener('input', () => {
                label.textContent = slider.value + (id === 'tilt' || id === 'tilt-rate' ? '°' : (id === 'strain' ? ' µε' : (id.includes('vib') ? 'g' : '')));
                runLiveMLInference();
            });
        }
    });

    const crackInput = document.getElementById('input-crack');
    if (crackInput) crackInput.addEventListener('change', runLiveMLInference);

    const btnNormal = document.getElementById('btn-preset-normal');
    const btnPre = document.getElementById('btn-preset-pre');
    const btnActive = document.getElementById('btn-preset-active');
    const btnBlast = document.getElementById('btn-preset-blast');

    if (btnNormal) btnNormal.addEventListener('click', () => setPreset(0.02, 0.0001, 0.5, 0.025, 0.06, 14.5, 1));
    if (btnPre) btnPre.addEventListener('click', () => setPreset(0.25, 0.008, 8.5, 0.045, 0.12, 10.2, 1));
    if (btnActive) btnActive.addEventListener('click', () => setPreset(1.45, 0.035, 32.0, 0.18, 0.65, 4.5, 0));
    if (btnBlast) btnBlast.addEventListener('click', () => setPreset(0.02, 0.0001, 0.5, 0.85, 2.1, 45.0, 1));

    runLiveMLInference();
}

function setPreset(tilt, tiltRate, strain, vibRms, vibPeak, vibFreq, crack) {
    const inTilt = document.getElementById('input-tilt');
    if (inTilt) { inTilt.value = tilt; document.getElementById('lbl-tilt').textContent = tilt + '°'; }

    const inTiltRate = document.getElementById('input-tilt-rate');
    if (inTiltRate) { inTiltRate.value = tiltRate; document.getElementById('lbl-tilt-rate').textContent = tiltRate + '°'; }

    const inStrain = document.getElementById('input-strain');
    if (inStrain) { inStrain.value = strain; document.getElementById('lbl-strain').textContent = strain + ' µε'; }

    const inVibRms = document.getElementById('input-vib-rms');
    if (inVibRms) { inVibRms.value = vibRms; document.getElementById('lbl-vib-rms').textContent = vibRms + 'g'; }

    const inVibPeak = document.getElementById('input-vib-peak');
    if (inVibPeak) { inVibPeak.value = vibPeak; document.getElementById('lbl-vib-peak').textContent = vibPeak + 'g'; }

    const inVibFreq = document.getElementById('input-vib-freq');
    if (inVibFreq) { inVibFreq.value = vibFreq; document.getElementById('lbl-vib-freq').textContent = vibFreq + ' Hz'; }

    const inCrack = document.getElementById('input-crack');
    if (inCrack) inCrack.value = crack;

    runLiveMLInference();
}

async function runLiveMLInference() {
    const inTilt = document.getElementById('input-tilt');
    if (!inTilt) return;

    const payload = {
        tilt_mean: parseFloat(inTilt.value),
        tilt_rate: parseFloat(document.getElementById('input-tilt-rate').value),
        strain_delta: parseFloat(document.getElementById('input-strain').value),
        vib_rms: parseFloat(document.getElementById('input-vib-rms').value),
        vib_peak: parseFloat(document.getElementById('input-vib-peak').value),
        vib_dominant_freq: parseFloat(document.getElementById('input-vib-freq').value),
        crack_status: parseInt(document.getElementById('input-crack').value),
        temp_humidity_index: parseFloat(document.getElementById('input-env').value)
    };

    try {
        const edgeRes = await fetch('/api/predict/edge', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const edgeData = await edgeRes.json();

        const edgeRating = document.getElementById('edge-rating');
        if (edgeRating) {
            edgeRating.textContent = edgeData.rating;
            edgeRating.className = 'val-bold ' + (edgeData.rating.includes('NORMAL') ? 'text-green-dark' : (edgeData.rating.includes('WARNING') ? 'warning-txt' : 'danger-txt'));
        }
        const edgeScore = document.getElementById('edge-score');
        if (edgeScore) edgeScore.textContent = edgeData.anomaly_score;
        const edgeSpeed = document.getElementById('edge-speed');
        if (edgeSpeed) edgeSpeed.textContent = `${edgeData.simulated_mcu_inference_us} µs`;

        const packets = { 'N2': payload, 'N3': payload, 'N4': payload };
        const gatewayRes = await fetch('/api/predict/gateway', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ packets })
        });
        const gatewayData = await gatewayRes.json();

        const gEvent = document.getElementById('gateway-event');
        if (gEvent) gEvent.textContent = gatewayData.event_type;
        const gBlast = document.getElementById('gateway-blast');
        if (gBlast) gBlast.textContent = gatewayData.event_type === 'BLAST_TRANSIENT' ? 'BLAST SUPPRESSED (Safe)' : 'No Blast Filtered';
        const gSiren = document.getElementById('gateway-siren');
        if (gSiren) gSiren.textContent = gatewayData.siren_trigger ? '🚨 SIREN FIRED' : 'Muted / Safe';

        updateDashboardAlertState(gatewayData, payload);
    } catch (err) {
        console.error("ML Inference API Error:", err);
    }
}

function updateDashboardAlertState(gatewayData, payload) {
    const alertBox = document.getElementById('alert-box');
    const alertIcon = document.getElementById('alert-icon');
    const alertTitle = document.getElementById('alert-title');
    const alertMsg = document.getElementById('alert-msg');
    
    const riskVal = document.getElementById('overall-risk-val');
    const riskBar = document.getElementById('risk-bar');
    
    const mTilt = document.getElementById('m-tilt');
    const mStrain = document.getElementById('m-strain');
    const statMaxTilt = document.getElementById('stat-max-tilt');
    const statMaxStrain = document.getElementById('stat-max-strain');
    const statSiren = document.getElementById('stat-siren');
    const statDisp = document.getElementById('stat-disp');

    if (mTilt) mTilt.textContent = `${payload.tilt_mean}°`;
    if (mStrain) mStrain.textContent = `${payload.strain_delta} µε`;
    if (statMaxTilt) statMaxTilt.textContent = `${payload.tilt_mean}°`;
    if (statMaxStrain) statMaxStrain.textContent = `${payload.strain_delta} µε`;
    if (statSiren) statSiren.textContent = gatewayData.siren_trigger ? '🚨 ACTIVE' : 'MUTED';

    if (gatewayData.event_type === 'BLAST_TRANSIENT') {
        if (alertBox) alertBox.className = 'alert-panel blast';
        if (alertIcon) alertIcon.textContent = '🟣';
        if (alertTitle) alertTitle.textContent = 'OPERATIONAL BLAST (FILTERED)';
        if (alertMsg) alertMsg.textContent = 'Transient blast vibration detected. Ground tilt/strain remains zero. Siren suppressed.';
        if (riskVal) riskVal.textContent = '0.12';
        if (riskBar) riskBar.style.width = '12%';
        const mRisk = document.getElementById('m-risk');
        if (mRisk) mRisk.textContent = '12.0%';
        const mRiskSub = document.getElementById('m-risk-sub');
        if (mRiskSub) mRiskSub.textContent = 'BLAST_FILTERED';
        updateNodeMapColors({'N1': 'blast', 'N2': 'blast', 'N3': 'blast', 'N4': 'blast', 'N5': 'blast'});
        stopSirenSound();
    } else if (gatewayData.event_type === 'SUBSIDENCE_PROGRESSION' || payload.crack_status === 0 || payload.tilt_mean > 1.0) {
        if (alertBox) alertBox.className = 'alert-panel critical';
        if (alertIcon) alertIcon.textContent = '🔴';
        if (alertTitle) alertTitle.textContent = 'CRITICAL SUBSIDENCE COLLAPSE ALERT!';
        if (alertMsg) alertMsg.textContent = gatewayData.summary || 'Surface panel experiencing rapid tilt and crack wire breakage. Evacuate longwall panel!';
        if (riskVal) riskVal.textContent = '0.94';
        if (riskBar) riskBar.style.width = '94%';
        const mRisk = document.getElementById('m-risk');
        if (mRisk) mRisk.textContent = '94.2%';
        const mRiskSub = document.getElementById('m-risk-sub');
        if (mRiskSub) mRiskSub.textContent = 'CRITICAL_ALERT';
        if (statDisp) statDisp.textContent = '42.5 mm';
        updateNodeMapColors({'N1': 'warning', 'N2': 'critical', 'N3': 'critical', 'N4': 'critical', 'N5': 'warning'});
        startSirenSound();
    } else if (gatewayData.event_type === 'EARLY_WARNING_OR_SENSOR_FAULT' || payload.tilt_mean > 0.1) {
        if (alertBox) alertBox.className = 'alert-panel warning';
        if (alertIcon) alertIcon.textContent = '🟡';
        if (alertTitle) alertTitle.textContent = 'PRE-SUBSIDENCE CREEP WARNING';
        if (alertMsg) alertMsg.textContent = 'Slow tilt ramp detected on center nodes. Monitoring deformation velocity.';
        if (riskVal) riskVal.textContent = '0.45';
        if (riskBar) riskBar.style.width = '45%';
        const mRisk = document.getElementById('m-risk');
        if (mRisk) mRisk.textContent = '45.0%';
        const mRiskSub = document.getElementById('m-risk-sub');
        if (mRiskSub) mRiskSub.textContent = 'PRE_SUBSIDENCE';
        if (statDisp) statDisp.textContent = '12.4 mm';
        updateNodeMapColors({'N1': 'normal', 'N2': 'warning', 'N3': 'warning', 'N4': 'normal', 'N5': 'normal'});
        stopSirenSound();
    } else {
        if (alertBox) alertBox.className = 'alert-panel normal';
        if (alertIcon) alertIcon.textContent = '🟢';
        if (alertTitle) alertTitle.textContent = 'NORMAL_STABLE';
        if (alertMsg) alertMsg.textContent = 'All surface mesh nodes report normal ground stability.';
        if (riskVal) riskVal.textContent = '0.02';
        if (riskBar) riskBar.style.width = '2%';
        const mRisk = document.getElementById('m-risk');
        if (mRisk) mRisk.textContent = '2.4%';
        const mRiskSub = document.getElementById('m-risk-sub');
        if (mRiskSub) mRiskSub.textContent = 'SAFE_STABLE';
        if (statDisp) statDisp.textContent = '0.0 mm';
        updateNodeMapColors({'N1': 'normal', 'N2': 'normal', 'N3': 'normal', 'N4': 'normal', 'N5': 'normal'});
        stopSirenSound();
    }
}

// ============================================================================
// 90-DAY SIMULATION PLAYER
// ============================================================================

let scenarioChart;

function initScenarioPlayer() {
    const buttons = document.querySelectorAll('.scen-card-btn');
    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadScenario(btn.dataset.scenario);
        });
    });

    loadScenario('normal');
}

function initScenarioChart() {
    const canvas = document.getElementById('scenarioChart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    scenarioChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: Array.from({length: 50}, (_, i) => `Window ${i+1}`),
            datasets: [
                { label: 'N3 Center Tilt (°)', borderColor: '#dc2626', backgroundColor: 'rgba(220, 38, 38, 0.08)', data: [], fill: true },
                { label: 'N3 Strain Delta (µε)', borderColor: '#d97706', backgroundColor: 'rgba(217, 119, 6, 0.08)', data: [], fill: true },
                { label: 'N3 Vibration RMS (g)', borderColor: '#9333ea', backgroundColor: 'rgba(147, 51, 234, 0.08)', data: [], fill: true }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#1e293b', font: { weight: '600' } } } },
            scales: {
                x: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#64748b' } },
                y: { grid: { color: 'rgba(0,0,0,0.05)' }, ticks: { color: '#64748b' } }
            }
        }
    });
}

async function loadScenario(scenarioName) {
    try {
        const res = await fetch(`/api/dataset/scenario/${scenarioName}`);
        const data = await res.json();
        
        const n3Data = data.nodes['N3'] || [];
        const tiltData = n3Data.map(d => d.tilt_mean);
        const strainData = n3Data.map(d => d.strain_delta);
        const vibData = n3Data.map(d => d.vib_rms);

        if (scenarioChart) {
            scenarioChart.data.datasets[0].data = tiltData;
            scenarioChart.data.datasets[1].data = strainData;
            scenarioChart.data.datasets[2].data = vibData;
            scenarioChart.update();
        }

        if (scenarioName === 'normal') setPreset(0.02, 0.0001, 0.5, 0.025, 0.06, 14.5, 1);
        else if (scenarioName === 'pre_subsidence') setPreset(0.25, 0.008, 8.5, 0.045, 0.12, 10.2, 1);
        else if (scenarioName === 'active') setPreset(1.45, 0.035, 32.0, 0.18, 0.65, 4.5, 0);
        else if (scenarioName === 'blast') setPreset(0.02, 0.0001, 0.5, 0.85, 2.1, 45.0, 1);

    } catch (err) {
        console.error("Scenario Load Error:", err);
    }
}
