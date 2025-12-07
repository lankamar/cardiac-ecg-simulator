/**
 * 🫀 Cardiac ECG Simulator - JavaScript Engine
 * 
 * Generates realistic ECG waveforms for 54 cardiac arrhythmias
 * with real-time visualization on HTML5 Canvas.
 */

// =============================================================================
// ARRHYTHMIA CONFIGURATIONS (54 types)
// =============================================================================

const ARRHYTHMIAS = {
    // Normal
    normal_sinus: {
        name: "Normal Sinus Rhythm",
        rate: [60, 100],
        hasP: true,
        pAmp: 0.15,
        qrsDuration: 80,
        qrsAmp: 1.0,
        tAmp: 0.3,
        prInterval: 160,
        regularity: 'regular',
        baseline: 'flat',
        mechanism: 'Normal',
        urgency: 'low'
    },

    // Supraventricular Brady
    sinus_bradycardia: {
        name: "Sinus Bradycardia",
        rate: [35, 59],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Decreased Automaticity', urgency: 'low'
    },
    sick_sinus: {
        name: "Sick Sinus Syndrome",
        rate: [30, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat',
        mechanism: 'Sinus Node Dysfunction', urgency: 'medium'
    },
    av_block_1: {
        name: "First Degree AV Block",
        rate: [50, 90],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 280, regularity: 'regular', baseline: 'flat',
        mechanism: 'Conduction Delay', urgency: 'low'
    },
    av_block_2_wenckebach: {
        name: "AV Block 2nd Wenckebach",
        rate: [40, 80],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 200, regularity: 'irregular', baseline: 'flat', pattern: 'wenckebach',
        mechanism: 'Progressive Block', urgency: 'medium'
    },
    av_block_2_mobitz: {
        name: "AV Block 2nd Mobitz II",
        rate: [30, 70],
        hasP: true, pAmp: 0.15, qrsDuration: 120, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 180, regularity: 'irregular', baseline: 'flat', pattern: 'mobitz',
        mechanism: 'Infranodal Block', urgency: 'high'
    },
    av_block_complete: {
        name: "Complete AV Block",
        rate: [30, 45],
        hasP: true, pAmp: 0.15, qrsDuration: 140, qrsAmp: 1.2, tAmp: 0.35,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'dissociation',
        mechanism: 'Complete Dissociation', urgency: 'critical'
    },

    // Supraventricular Tachy
    sinus_tachycardia: {
        name: "Sinus Tachycardia",
        rate: [100, 180],
        hasP: true, pAmp: 0.18, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 140, regularity: 'regular', baseline: 'flat',
        mechanism: 'Increased Automaticity', urgency: 'low'
    },
    atrial_fibrillation: {
        name: "Atrial Fibrillation",
        rate: [60, 160],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 0, regularity: 'chaotic', baseline: 'fibrillatory',
        mechanism: 'Multiple Reentry', urgency: 'medium'
    },
    atrial_flutter: {
        name: "Atrial Flutter",
        rate: [130, 150],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flutter',
        mechanism: 'Macro-Reentry', urgency: 'medium'
    },
    avnrt: {
        name: "AVNRT",
        rate: [140, 220],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 80, regularity: 'regular', baseline: 'flat',
        mechanism: 'Nodal Reentry', urgency: 'medium'
    },
    avrt: {
        name: "AVRT",
        rate: [140, 250],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 100, regularity: 'regular', baseline: 'flat',
        mechanism: 'Accessory Pathway', urgency: 'medium'
    },
    wpw: {
        name: "WPW Syndrome",
        rate: [100, 250],
        hasP: true, pAmp: 0.15, qrsDuration: 130, qrsAmp: 1.2, tAmp: 0.3,
        prInterval: 100, regularity: 'regular', baseline: 'flat', pattern: 'delta',
        mechanism: 'Preexcitation', urgency: 'high'
    },
    psvt: {
        name: "PSVT",
        rate: [150, 220],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Reentry', urgency: 'medium'
    },
    mat: {
        name: "Multifocal Atrial Tachycardia",
        rate: [100, 180],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'mat',
        mechanism: 'Multiple Foci', urgency: 'medium'
    },

    // Ventricular
    pvc: {
        name: "PVC",
        rate: [60, 100],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.8, tAmp: 0.5, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'pvc',
        mechanism: 'Ectopic Focus', urgency: 'low'
    },
    pvc_bigeminy: {
        name: "PVC Bigeminy",
        rate: [60, 100],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.8, tAmp: 0.5, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'bigeminy',
        mechanism: 'Alternating Ectopy', urgency: 'medium'
    },
    pvc_trigeminy: {
        name: "PVC Trigeminy",
        rate: [60, 100],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.8, tAmp: 0.5, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'trigeminy',
        mechanism: 'Patterned Ectopy', urgency: 'medium'
    },
    vt_mono: {
        name: "VT Monomorphic",
        rate: [140, 220],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ventricular Reentry', urgency: 'critical'
    },
    vt_poly: {
        name: "VT Polymorphic",
        rate: [100, 250],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0, tPolarity: -1,
        prInterval: 0, regularity: 'irregular', baseline: 'flat',
        mechanism: 'Multiple Reentry', urgency: 'critical'
    },
    torsades: {
        name: "Torsades de Pointes",
        rate: [200, 300],
        hasP: false, pAmp: 0, qrsDuration: 150, qrsAmp: 1.2, tAmp: 0, tPolarity: -1,
        prInterval: 0, regularity: 'irregular', baseline: 'torsades',
        mechanism: 'Triggered Activity', urgency: 'critical'
    },
    vf_coarse: {
        name: "VF Coarse",
        rate: [300, 500],
        hasP: false, pAmp: 0, qrsDuration: 0, qrsAmp: 0.8, tAmp: 0,
        prInterval: 0, regularity: 'chaotic', baseline: 'vf_coarse',
        mechanism: 'Chaotic Reentry', urgency: 'critical'
    },
    vf_fine: {
        name: "VF Fine",
        rate: [300, 500],
        hasP: false, pAmp: 0, qrsDuration: 0, qrsAmp: 0.3, tAmp: 0,
        prInterval: 0, regularity: 'chaotic', baseline: 'vf_fine',
        mechanism: 'Chaotic Reentry', urgency: 'critical'
    },
    asystole: {
        name: "Asystole",
        rate: [0, 0],
        hasP: false, pAmp: 0, qrsDuration: 0, qrsAmp: 0, tAmp: 0,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'No Activity', urgency: 'critical'
    },

    // Special
    brugada: {
        name: "Brugada Pattern",
        rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.0, tAmp: 0.2, tPolarity: -1,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'brugada',
        mechanism: 'Channelopathy', urgency: 'high'
    },
    r_on_t: {
        name: "R-on-T Phenomenon",
        rate: [60, 100],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.8, tAmp: 0.5, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'r_on_t',
        mechanism: 'Vulnerable Period', urgency: 'critical'
    },
    fusion: {
        name: "Fusion Beat",
        rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.2, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'fusion',
        mechanism: 'Dual Activation', urgency: 'low'
    }
};

// =============================================================================
// ECG SIMULATOR CLASS
// =============================================================================

class ECGSimulator {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.isRunning = false;
        this.currentArrhythmia = ARRHYTHMIAS.normal_sinus;
        this.heartRate = 75;
        this.noiseLevel = 0.02;
        this.speed = 25; // mm/s
        this.lead = 'II';

        // Drawing state
        this.x = 0;
        this.lastY = 0;
        this.beatPhase = 0;
        this.beatCount = 0;
        this.lastBeatTime = 0;

        // ECG trace buffer
        this.traceBuffer = [];
        this.maxBufferSize = 2000;

        this.setupCanvas();
        this.setupEventListeners();
    }

    setupCanvas() {
        const resize = () => {
            const wrapper = this.canvas.parentElement;
            this.canvas.width = wrapper.clientWidth;
            this.canvas.height = wrapper.clientHeight;
            this.centerY = this.canvas.height / 2;
            this.amplitude = this.canvas.height / 4;
        };

        resize();
        window.addEventListener('resize', resize);
    }

    setupEventListeners() {
        // Arrhythmia selector
        document.getElementById('arrhythmiaSelect').addEventListener('change', (e) => {
            this.setArrhythmia(e.target.value);
        });

        // Sliders
        document.getElementById('hrSlider').addEventListener('input', (e) => {
            this.heartRate = parseInt(e.target.value);
            document.getElementById('hrValue').textContent = `${this.heartRate} bpm`;
        });

        document.getElementById('noiseSlider').addEventListener('input', (e) => {
            this.noiseLevel = parseInt(e.target.value) / 100;
            document.getElementById('noiseValue').textContent = `${e.target.value}%`;
        });

        document.getElementById('speedSlider').addEventListener('input', (e) => {
            this.speed = parseInt(e.target.value);
            document.getElementById('speedValue').textContent = e.target.value;
        });

        // Buttons
        document.getElementById('startBtn').addEventListener('click', () => this.start());
        document.getElementById('stopBtn').addEventListener('click', () => this.stop());

        // Lead tabs
        document.querySelectorAll('.lead-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                document.querySelectorAll('.lead-tab').forEach(t => t.classList.remove('active'));
                e.target.classList.add('active');
                this.lead = e.target.dataset.lead;
            });
        });
    }

    setArrhythmia(key) {
        this.currentArrhythmia = ARRHYTHMIAS[key] || ARRHYTHMIAS.normal_sinus;
        this.updateUI();
        this.traceBuffer = [];
        this.x = 0;
    }

    updateUI() {
        const arr = this.currentArrhythmia;

        // Update header
        document.getElementById('currentName').textContent = arr.name;

        // Update urgency badge
        const badge = document.getElementById('urgencyBadge');
        badge.textContent = arr.urgency.toUpperCase();
        badge.className = `urgency-badge urgency-${arr.urgency}`;

        // Update stats
        const rate = Math.round((arr.rate[0] + arr.rate[1]) / 2);
        document.getElementById('statHR').textContent = rate || '--';
        document.getElementById('statQRS').textContent = arr.qrsDuration || '--';
        document.getElementById('statPR').textContent = arr.prInterval || '--';
        document.getElementById('statQT').textContent = arr.prInterval + arr.qrsDuration + 200 || '--';

        // Update info panel
        document.getElementById('infoRate').innerHTML = `${rate}<span class="info-card-unit">bpm</span>`;
        document.getElementById('infoMechanism').textContent = arr.mechanism;
        document.getElementById('infoQRS').textContent = arr.qrsDuration > 100 ? 'Wide' : 'Narrow';
        document.getElementById('infoRegularity').textContent = arr.regularity.charAt(0).toUpperCase() + arr.regularity.slice(1);

        // Update HR slider
        document.getElementById('hrSlider').value = rate;
        document.getElementById('hrValue').textContent = `${rate} bpm`;
        this.heartRate = rate;
    }

    // ==========================================================================
    // WAVEFORM GENERATION
    // ==========================================================================

    generateWaveform(t, rrInterval) {
        const arr = this.currentArrhythmia;

        // Handle special baselines
        if (arr.baseline === 'vf_coarse') return this.generateVFCoarse(t);
        if (arr.baseline === 'vf_fine') return this.generateVFFine(t);
        if (arr.baseline === 'torsades') return this.generateTorsades(t);
        if (arr.baseline === 'asystole' || arr.rate[1] === 0) return this.addNoise(0);

        // Normalize time within beat cycle
        const cycleT = (t % rrInterval) / rrInterval;

        let y = 0;

        // Add baseline patterns
        if (arr.baseline === 'fibrillatory') {
            y += 0.05 * (Math.random() - 0.5);
        } else if (arr.baseline === 'flutter') {
            y += 0.15 * this.generateFlutterWave(t);
        }

        // P wave (if present)
        if (arr.hasP && cycleT < 0.15) {
            const pT = cycleT / 0.15;
            y += arr.pAmp * this.gaussian(pT, 0.5, 0.2);
        }

        // QRS complex
        if (cycleT >= 0.2 && cycleT < 0.35) {
            const qrsT = (cycleT - 0.2) / 0.15;
            y += this.generateQRS(qrsT, arr);
        }

        // T wave
        if (arr.tAmp > 0 && cycleT >= 0.4 && cycleT < 0.65) {
            const tT = (cycleT - 0.4) / 0.25;
            const polarity = arr.tPolarity || 1;
            y += arr.tAmp * polarity * this.gaussian(tT, 0.5, 0.25);
        }

        return this.addNoise(y);
    }

    generateQRS(t, arr) {
        const amp = arr.qrsAmp;

        // Check for delta wave (WPW)
        if (arr.pattern === 'delta') {
            if (t < 0.2) {
                return amp * 0.3 * t / 0.2; // Slurred upstroke
            }
            t = (t - 0.2) / 0.8;
        }

        // Standard QRS
        if (t < 0.2) {
            return -0.15 * amp * Math.sin(t / 0.2 * Math.PI); // Q
        } else if (t < 0.5) {
            return amp * Math.sin((t - 0.2) / 0.3 * Math.PI); // R
        } else {
            return -0.3 * amp * Math.sin((t - 0.5) / 0.5 * Math.PI); // S
        }
    }

    generateVFCoarse(t) {
        let y = 0;
        for (let i = 0; i < 5; i++) {
            const freq = 4 + i;
            y += 0.6 * Math.sin(2 * Math.PI * freq * t / 1000 + i);
        }
        y *= 0.5 + 0.5 * Math.sin(2 * Math.PI * 0.5 * t / 1000);
        return this.addNoise(y * 0.4);
    }

    generateVFFine(t) {
        let y = 0;
        for (let i = 0; i < 4; i++) {
            const freq = 5 + i;
            y += 0.3 * Math.sin(2 * Math.PI * freq * t / 1000 + i);
        }
        return this.addNoise(y * 0.2);
    }

    generateTorsades(t) {
        const baseFreq = 4;
        const modFreq = 0.5;
        const modulation = Math.sin(2 * Math.PI * modFreq * t / 1000);
        const y = Math.sin(2 * Math.PI * baseFreq * t / 1000) * (0.5 + 0.5 * modulation);
        return this.addNoise(y * 0.8);
    }

    generateFlutterWave(t) {
        const period = 200; // 300 bpm flutter
        const phase = (t % period) / period;
        return 2 * phase - 1; // Sawtooth
    }

    gaussian(x, mean, sigma) {
        return Math.exp(-Math.pow(x - mean, 2) / (2 * sigma * sigma));
    }

    addNoise(y) {
        return y + this.noiseLevel * (Math.random() - 0.5) * 2;
    }

    // ==========================================================================
    // ANIMATION LOOP
    // ==========================================================================

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.traceBuffer = [];
        this.x = 0;
        this.lastTime = performance.now();
        this.animate();
    }

    stop() {
        this.isRunning = false;
    }

    animate() {
        if (!this.isRunning) return;

        const now = performance.now();
        const dt = now - this.lastTime;
        this.lastTime = now;

        // Calculate RR interval
        const rate = this.heartRate || 75;
        const rrInterval = 60000 / rate; // ms

        // Pixels per ms based on speed
        const pixelsPerMs = (this.speed * this.canvas.width) / (25 * 4000);

        // Generate new samples
        const samplesToGenerate = Math.ceil(dt * pixelsPerMs);

        for (let i = 0; i < samplesToGenerate; i++) {
            const t = now + i;
            const y = this.generateWaveform(t, rrInterval);

            this.traceBuffer.push({
                x: this.x,
                y: this.centerY - y * this.amplitude
            });

            this.x += 1;
            if (this.x > this.canvas.width) {
                this.x = 0;
                this.traceBuffer = [];
            }
        }

        // Limit buffer size
        if (this.traceBuffer.length > this.maxBufferSize) {
            this.traceBuffer = this.traceBuffer.slice(-this.maxBufferSize);
        }

        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    draw() {
        // Clear with transparency for trace persistence
        this.ctx.fillStyle = 'rgba(10, 15, 26, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        if (this.traceBuffer.length < 2) return;

        // Draw trace
        this.ctx.beginPath();
        this.ctx.strokeStyle = '#10b981';
        this.ctx.lineWidth = 2;
        this.ctx.shadowColor = '#10b981';
        this.ctx.shadowBlur = 10;

        this.ctx.moveTo(this.traceBuffer[0].x, this.traceBuffer[0].y);

        for (let i = 1; i < this.traceBuffer.length; i++) {
            this.ctx.lineTo(this.traceBuffer[i].x, this.traceBuffer[i].y);
        }

        this.ctx.stroke();

        // Draw current position marker
        const last = this.traceBuffer[this.traceBuffer.length - 1];
        this.ctx.beginPath();
        this.ctx.arc(last.x, last.y, 4, 0, Math.PI * 2);
        this.ctx.fillStyle = '#10b981';
        this.ctx.fill();
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const simulator = new ECGSimulator('ecgCanvas');
    simulator.start();
});
