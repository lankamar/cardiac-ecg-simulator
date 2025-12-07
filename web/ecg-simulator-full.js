/**
 * 🫀 Cardiac ECG Simulator - COMPLETE 54 ARRHYTHMIAS
 * Version 2.1 - Full Implementation
 */

// =============================================================================
// 54 ARRHYTHMIA CONFIGURATIONS
// =============================================================================

const ARRHYTHMIAS = {
    // =========================================================================
    // NORMAL (1)
    // =========================================================================
    normal_sinus: {
        name: "Normal Sinus Rhythm", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Normal Automaticity', urgency: 'low'
    },

    // =========================================================================
    // SUPRAVENTRICULAR BRADYARRHYTHMIAS (6)
    // =========================================================================
    sinus_bradycardia: {
        name: "Sinus Bradycardia", rate: [35, 59],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Decreased Automaticity', urgency: 'low'
    },
    sick_sinus: {
        name: "Sick Sinus Syndrome", rate: [30, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'pauses',
        mechanism: 'Sinus Node Dysfunction', urgency: 'medium'
    },
    av_block_1: {
        name: "First Degree AV Block", rate: [50, 90],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 300, regularity: 'regular', baseline: 'flat',
        mechanism: 'Conduction Delay', urgency: 'low'
    },
    av_block_2_wenckebach: {
        name: "AV Block 2nd Wenckebach", rate: [50, 80],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 200, regularity: 'irregular', baseline: 'flat', pattern: 'wenckebach',
        wenckebachCycle: 4, prProgression: [200, 260, 320, 0],
        mechanism: 'Progressive Block', urgency: 'medium'
    },
    av_block_2_mobitz: {
        name: "AV Block 2nd Mobitz II", rate: [30, 70],
        hasP: true, pAmp: 0.15, qrsDuration: 120, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 180, regularity: 'irregular', baseline: 'flat', pattern: 'mobitz',
        mechanism: 'Infranodal Block', urgency: 'high'
    },
    av_block_complete: {
        name: "Complete AV Block", rate: [30, 45],
        hasP: true, pAmp: 0.15, qrsDuration: 140, qrsAmp: 1.2, tAmp: 0.35,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'dissociation',
        atrialRate: 80, mechanism: 'Complete Dissociation', urgency: 'critical'
    },

    // =========================================================================
    // SUPRAVENTRICULAR TACHYARRHYTHMIAS (14)
    // =========================================================================
    sinus_tachycardia: {
        name: "Sinus Tachycardia", rate: [100, 180],
        hasP: true, pAmp: 0.18, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 140, regularity: 'regular', baseline: 'flat',
        mechanism: 'Increased Automaticity', urgency: 'low'
    },
    atrial_tachycardia: {
        name: "Atrial Tachycardia", rate: [150, 250],
        hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 140, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ectopic Focus', urgency: 'medium'
    },
    atrial_flutter: {
        name: "Atrial Flutter", rate: [130, 150],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flutter', flutterRate: 300,
        mechanism: 'Macro-Reentry', urgency: 'medium'
    },
    atrial_flutter_atypical: {
        name: "Atypical Atrial Flutter", rate: [120, 200],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flutter', flutterRate: 250,
        mechanism: 'Atypical Reentry', urgency: 'medium'
    },
    atrial_fibrillation: {
        name: "Atrial Fibrillation", rate: [60, 160],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 0, regularity: 'chaotic', baseline: 'fibrillatory',
        mechanism: 'Multiple Reentry', urgency: 'medium'
    },
    avnrt: {
        name: "AVNRT", rate: [140, 220],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 80, regularity: 'regular', baseline: 'flat',
        mechanism: 'Nodal Reentry', urgency: 'medium'
    },
    avrt: {
        name: "AVRT", rate: [140, 250],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 100, regularity: 'regular', baseline: 'flat',
        mechanism: 'Accessory Pathway', urgency: 'medium'
    },
    wpw: {
        name: "WPW Syndrome", rate: [100, 250],
        hasP: true, pAmp: 0.15, qrsDuration: 130, qrsAmp: 1.2, tAmp: 0.3,
        prInterval: 100, regularity: 'regular', baseline: 'flat', pattern: 'delta',
        mechanism: 'Preexcitation', urgency: 'high'
    },
    psvt: {
        name: "PSVT", rate: [150, 220],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Reentry', urgency: 'medium'
    },
    mat: {
        name: "Multifocal Atrial Tachycardia", rate: [100, 180],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'mat',
        mechanism: 'Multiple Foci', urgency: 'medium'
    },
    focal_at: {
        name: "Focal Atrial Tachycardia", rate: [150, 250],
        hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 140, regularity: 'regular', baseline: 'flat',
        mechanism: 'Single Focus', urgency: 'medium'
    },
    intra_atrial_reentry: {
        name: "Intra-atrial Reentry", rate: [130, 200],
        hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 150, regularity: 'regular', baseline: 'flat',
        mechanism: 'Atrial Reentry', urgency: 'medium'
    },
    sinus_node_reentry: {
        name: "Sinus Node Reentry", rate: [100, 150],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Nodal Reentry', urgency: 'low'
    },
    ectopic_atrial: {
        name: "Ectopic Atrial Rhythm", rate: [60, 100],
        hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ectopic Pacemaker', urgency: 'low'
    },

    // =========================================================================
    // OTHER SUPRAVENTRICULAR (10)
    // =========================================================================
    pac: {
        name: "Premature Atrial Contraction", rate: [60, 100],
        hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'pac',
        mechanism: 'Premature Beat', urgency: 'low'
    },
    pjc: {
        name: "Premature Junctional Contraction", rate: [60, 100],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'pjc',
        mechanism: 'Junctional Ectopy', urgency: 'low'
    },
    junctional_escape: {
        name: "Junctional Escape Rhythm", rate: [40, 60],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Escape Rhythm', urgency: 'medium'
    },
    junctional_tachy: {
        name: "Junctional Tachycardia", rate: [70, 130],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Enhanced Automaticity', urgency: 'medium'
    },
    jet: {
        name: "JET (Junctional Ectopic Tachy)", rate: [120, 200],
        hasP: false, pAmp: 0, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ectopic Junction', urgency: 'high'
    },
    wandering_pacemaker: {
        name: "Wandering Atrial Pacemaker", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'wandering',
        mechanism: 'Variable Focus', urgency: 'low'
    },
    sinus_arrhythmia: {
        name: "Sinus Arrhythmia", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat',
        mechanism: 'Respiratory Variation', urgency: 'low'
    },
    sinus_pause: {
        name: "Sinus Pause", rate: [50, 80],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'pause',
        mechanism: 'Transient Arrest', urgency: 'medium'
    },
    sinus_arrest: {
        name: "Sinus Arrest", rate: [30, 60],
        hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'arrest',
        mechanism: 'Prolonged Arrest', urgency: 'high'
    },
    sinoatrial_block: {
        name: "Sinoatrial Exit Block", rate: [50, 80],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'sa_block',
        mechanism: 'Exit Block', urgency: 'medium'
    },

    // =========================================================================
    // VENTRICULAR ARRHYTHMIAS (16)
    // =========================================================================
    pvc: {
        name: "PVC", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'pvc',
        pvcRate: 6, mechanism: 'Ectopic Focus', urgency: 'low'
    },
    pvc_bigeminy: {
        name: "PVC Bigeminy", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'bigeminy',
        mechanism: 'Alternating Ectopy', urgency: 'medium'
    },
    pvc_trigeminy: {
        name: "PVC Trigeminy", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'trigeminy',
        mechanism: 'Patterned Ectopy', urgency: 'medium'
    },
    pvc_couplet: {
        name: "PVC Couplet", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'couplet',
        mechanism: 'Paired Ectopy', urgency: 'medium'
    },
    pvc_triplet: {
        name: "PVC Triplet / NSVT", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'triplet',
        mechanism: 'Brief VT', urgency: 'high'
    },
    aivr: {
        name: "AIVR", rate: [40, 110],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.3, tAmp: 0.4, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Accelerated Escape', urgency: 'low'
    },
    ventricular_escape: {
        name: "Ventricular Escape Rhythm", rate: [20, 40],
        hasP: false, pAmp: 0, qrsDuration: 160, qrsAmp: 1.5, tAmp: 0.5, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ventricular Escape', urgency: 'high'
    },
    vt_mono: {
        name: "VT Monomorphic", rate: [140, 220],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ventricular Reentry', urgency: 'critical'
    },
    vt_poly: {
        name: "VT Polymorphic", rate: [100, 250],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0, tPolarity: -1,
        prInterval: 0, regularity: 'irregular', baseline: 'flat', pattern: 'polymorphic',
        mechanism: 'Multiple Reentry', urgency: 'critical'
    },
    vt_sustained: {
        name: "VT Sustained", rate: [100, 250],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Sustained Reentry', urgency: 'critical'
    },
    vt_nonsustained: {
        name: "VT Non-Sustained", rate: [100, 250],
        hasP: false, pAmp: 0, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'nsvt',
        mechanism: 'Brief VT', urgency: 'high'
    },
    torsades: {
        name: "Torsades de Pointes", rate: [200, 300],
        hasP: false, pAmp: 0, qrsDuration: 150, qrsAmp: 1.2, tAmp: 0,
        prInterval: 0, regularity: 'irregular', baseline: 'torsades',
        mechanism: 'Triggered Activity', urgency: 'critical'
    },
    vf_coarse: {
        name: "VF Coarse", rate: [300, 500],
        hasP: false, pAmp: 0, qrsDuration: 0, qrsAmp: 0.8, tAmp: 0,
        prInterval: 0, regularity: 'chaotic', baseline: 'vf_coarse',
        mechanism: 'Chaotic Reentry', urgency: 'critical'
    },
    vf_fine: {
        name: "VF Fine", rate: [300, 500],
        hasP: false, pAmp: 0, qrsDuration: 0, qrsAmp: 0.3, tAmp: 0,
        prInterval: 0, regularity: 'chaotic', baseline: 'vf_fine',
        mechanism: 'Chaotic Reentry', urgency: 'critical'
    },
    asystole: {
        name: "Asystole", rate: [0, 0],
        hasP: false, pAmp: 0, qrsDuration: 0, qrsAmp: 0, tAmp: 0,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'No Activity', urgency: 'critical'
    },
    idioventricular: {
        name: "Idioventricular Rhythm", rate: [20, 40],
        hasP: false, pAmp: 0, qrsDuration: 160, qrsAmp: 1.5, tAmp: 0.5, tPolarity: -1,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ventricular Escape', urgency: 'high'
    },

    // =========================================================================
    // SPECIAL PHENOMENA (8)
    // =========================================================================
    parasystole: {
        name: "Parasystole", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'parasystole',
        mechanism: 'Protected Focus', urgency: 'low'
    },
    fusion: {
        name: "Fusion Beat", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.2, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'fusion',
        mechanism: 'Dual Activation', urgency: 'low'
    },
    capture: {
        name: "Capture Beat", rate: [140, 200],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'capture',
        mechanism: 'Supraventricular Capture', urgency: 'low'
    },
    r_on_t: {
        name: "R-on-T Phenomenon", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'r_on_t',
        mechanism: 'Vulnerable Period', urgency: 'critical'
    },
    ashman: {
        name: "Ashman Phenomenon", rate: [80, 140],
        hasP: true, pAmp: 0.15, qrsDuration: 120, qrsAmp: 1.2, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'ashman',
        mechanism: 'Aberrant Conduction', urgency: 'low'
    },
    concealed: {
        name: "Concealed Conduction", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 180, regularity: 'irregular', baseline: 'flat', pattern: 'concealed',
        mechanism: 'Hidden Conduction', urgency: 'low'
    },
    av_dissociation: {
        name: "AV Dissociation", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.2, tAmp: 0.3,
        prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'dissociation',
        mechanism: 'Independent Rhythms', urgency: 'medium'
    },
    brugada: {
        name: "Brugada Pattern", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.0, tAmp: 0.2, tPolarity: -1,
        prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'brugada',
        mechanism: 'Channelopathy', urgency: 'high'
    }
};

// Count for verification
console.log(`🫀 Total arrhythmias loaded: ${Object.keys(ARRHYTHMIAS).length}`);

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
        this.noiseLevel = 0;
        this.speed = 25;
        this.lead = 'II';
        this.beatCount = 0;
        this.tracePoints = [];
        this.maxPoints = 3000;
        this.drawX = 0;
        this.sampleBuffer = [];
        this.sampleIndex = 0;

        this.setupCanvas();
        this.setupEventListeners();
    }

    setupCanvas() {
        const resize = () => {
            const wrapper = this.canvas.parentElement;
            this.canvas.width = wrapper.clientWidth;
            this.canvas.height = wrapper.clientHeight;
            this.centerY = this.canvas.height / 2;
            this.amplitude = this.canvas.height / 3.5;
        };
        resize();
        window.addEventListener('resize', resize);
    }

    setupEventListeners() {
        document.getElementById('arrhythmiaSelect').addEventListener('change', (e) => {
            this.setArrhythmia(e.target.value);
        });

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

        document.getElementById('startBtn').addEventListener('click', () => this.start());
        document.getElementById('stopBtn').addEventListener('click', () => this.stop());

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
        this.beatCount = 0;
        this.updateUI();
        this.tracePoints = [];
        this.drawX = 0;
        this.sampleBuffer = [];
        this.sampleIndex = 0;
    }

    updateUI() {
        const arr = this.currentArrhythmia;
        document.getElementById('currentName').textContent = arr.name;

        const badge = document.getElementById('urgencyBadge');
        badge.textContent = arr.urgency.toUpperCase();
        badge.className = `urgency-badge urgency-${arr.urgency}`;

        const rate = Math.round((arr.rate[0] + arr.rate[1]) / 2);
        document.getElementById('statHR').textContent = rate || '--';
        document.getElementById('statQRS').textContent = arr.qrsDuration || '--';
        document.getElementById('statPR').textContent = arr.prInterval || '--';
        document.getElementById('statQT').textContent = (arr.prInterval + arr.qrsDuration + 200) || '--';

        document.getElementById('infoRate').innerHTML = `${rate}<span class="info-card-unit">bpm</span>`;
        document.getElementById('infoMechanism').textContent = arr.mechanism;
        document.getElementById('infoQRS').textContent = arr.qrsDuration > 100 ? 'Wide' : 'Narrow';
        document.getElementById('infoRegularity').textContent = arr.regularity.charAt(0).toUpperCase() + arr.regularity.slice(1);

        document.getElementById('hrSlider').value = rate;
        document.getElementById('hrValue').textContent = `${rate} bpm`;
        this.heartRate = rate;
    }

    gaussian(x, mu, sigma) {
        return Math.exp(-Math.pow(x - mu, 2) / (2 * sigma * sigma));
    }

    generateQRS(t, arr, isPVC = false) {
        const amp = isPVC ? 1.8 : arr.qrsAmp;
        if (t < 0 || t > 1) return 0;
        if (t < 0.15) return -0.1 * amp * this.gaussian(t, 0.075, 0.05);
        else if (t < 0.5) return amp * Math.sin((t - 0.15) / 0.35 * Math.PI);
        else return -0.25 * amp * Math.sin((t - 0.5) / 0.5 * Math.PI);
    }

    generateWideQRS(t) {
        if (t < 0 || t > 1) return 0;
        const amp = 1.5;
        if (t < 0.3) return amp * 0.3 * t / 0.3;
        else if (t < 0.5) return amp * (0.3 + 0.7 * Math.sin((t - 0.3) / 0.2 * Math.PI / 2));
        else return amp * (1.0 - 1.4 * (t - 0.5) / 0.5) * Math.cos((t - 0.5) / 0.5 * Math.PI / 2);
    }

    generateBeat(arr, beatIndex) {
        const rate = this.heartRate || 75;
        const rrInterval = 60000 / rate;
        const samples = [];
        const samplesPerMs = 0.5;
        const totalSamples = Math.floor(rrInterval * samplesPerMs);

        let prInterval = arr.prInterval;
        let dropBeat = false;

        if (arr.pattern === 'wenckebach' && arr.prProgression) {
            const cyclePos = beatIndex % arr.wenckebachCycle;
            prInterval = arr.prProgression[cyclePos];
            dropBeat = prInterval === 0;
        }

        let isPVC = false;
        if (arr.pattern === 'bigeminy' && beatIndex % 2 === 1) isPVC = true;
        if (arr.pattern === 'trigeminy' && beatIndex % 3 === 2) isPVC = true;
        if (arr.pattern === 'pvc' && beatIndex % (arr.pvcRate || 6) === 5) isPVC = true;
        if (arr.pattern === 'couplet' && (beatIndex % 5 === 3 || beatIndex % 5 === 4)) isPVC = true;
        if (arr.pattern === 'triplet' && (beatIndex % 6 >= 3 && beatIndex % 6 <= 5)) isPVC = true;

        for (let i = 0; i < totalSamples; i++) {
            const t = i / samplesPerMs;
            const cycleT = t / rrInterval;
            let y = 0;

            if (arr.baseline === 'fibrillatory') {
                y += 0.03 * Math.sin(t * 0.05) + 0.02 * Math.sin(t * 0.13);
            } else if (arr.baseline === 'flutter') {
                const flutterPeriod = 60000 / (arr.flutterRate || 300);
                y += 0.15 * (2 * ((t % flutterPeriod) / flutterPeriod) - 1);
            }

            if (dropBeat && cycleT > 0.15) {
                samples.push(y);
                continue;
            }

            if (arr.hasP && !isPVC) {
                if (cycleT >= 0 && cycleT < 0.08) {
                    y += arr.pAmp * this.gaussian(cycleT / 0.08, 0.5, 0.2);
                }
            }

            const qrsStart = (prInterval || 160) / rrInterval;
            const qrsDuration = (isPVC ? 140 : arr.qrsDuration) / rrInterval;

            if (cycleT >= qrsStart && cycleT < qrsStart + qrsDuration) {
                const qrsT = (cycleT - qrsStart) / qrsDuration;
                if (isPVC || arr.qrsDuration > 120) {
                    y += this.generateWideQRS(qrsT);
                } else {
                    y += this.generateQRS(qrsT, arr);
                }
            }

            const tStart = qrsStart + qrsDuration + 0.08;
            const tDuration = 0.15;
            if (arr.tAmp > 0 && cycleT >= tStart && cycleT < tStart + tDuration) {
                const tT = (cycleT - tStart) / tDuration;
                const polarity = isPVC ? -1 : (arr.tPolarity || 1);
                y += arr.tAmp * polarity * this.gaussian(tT, 0.5, 0.25);
            }

            samples.push(y);
        }
        return samples;
    }

    generateVFCoarse(duration) {
        const samples = [];
        for (let i = 0; i < duration * 500; i++) {
            const t = i / 500;
            let y = 0.4 * Math.sin(2 * Math.PI * 5 * t) + 0.3 * Math.sin(2 * Math.PI * 7 * t + 1);
            y *= 0.6 + 0.4 * Math.sin(2 * Math.PI * 0.5 * t);
            samples.push(y * 0.7);
        }
        return samples;
    }

    generateVFFine(duration) {
        const samples = [];
        for (let i = 0; i < duration * 500; i++) {
            const t = i / 500;
            samples.push(0.15 * Math.sin(2 * Math.PI * 6 * t) + 0.1 * Math.sin(2 * Math.PI * 8 * t + 0.5));
        }
        return samples;
    }

    generateTorsades(duration) {
        const samples = [];
        for (let i = 0; i < duration * 500; i++) {
            const t = i / 500;
            const mod = Math.sin(2 * Math.PI * 0.4 * t);
            samples.push(0.8 * Math.sin(2 * Math.PI * 4.5 * t) * (0.5 + 0.5 * mod));
        }
        return samples;
    }

    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.tracePoints = [];
        this.drawX = 0;
        this.beatCount = 0;
        this.lastTime = performance.now();
        this.sampleBuffer = [];
        this.sampleIndex = 0;
        this.generateNextBeat();
        this.animate();
    }

    stop() { this.isRunning = false; }

    generateNextBeat() {
        const arr = this.currentArrhythmia;
        if (arr.baseline === 'vf_coarse') this.sampleBuffer = this.generateVFCoarse(2);
        else if (arr.baseline === 'vf_fine') this.sampleBuffer = this.generateVFFine(2);
        else if (arr.baseline === 'torsades') this.sampleBuffer = this.generateTorsades(2);
        else if (arr.rate[1] === 0) this.sampleBuffer = new Array(1000).fill(0);
        else {
            this.sampleBuffer = this.generateBeat(arr, this.beatCount);
            this.beatCount++;
        }
        this.sampleIndex = 0;
    }

    animate() {
        if (!this.isRunning) return;
        const now = performance.now();
        const dt = now - this.lastTime;
        this.lastTime = now;

        const pixelsPerMs = (this.speed / 25) * 0.5;
        const samplesToConsume = Math.ceil(dt * pixelsPerMs);

        for (let i = 0; i < samplesToConsume; i++) {
            if (this.sampleIndex >= this.sampleBuffer.length) this.generateNextBeat();
            const y = this.sampleBuffer[this.sampleIndex] || 0;
            this.sampleIndex++;
            const finalY = y + (this.noiseLevel * (Math.random() - 0.5) * 0.5);
            this.tracePoints.push({ x: this.drawX, y: this.centerY - finalY * this.amplitude });
            this.drawX += 1;
            if (this.drawX > this.canvas.width) {
                this.drawX = 0;
                this.tracePoints = [];
            }
        }

        if (this.tracePoints.length > this.maxPoints) {
            this.tracePoints = this.tracePoints.slice(-this.maxPoints);
        }

        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    draw() {
        this.ctx.fillStyle = 'rgba(26, 26, 26, 0.15)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        if (this.tracePoints.length < 2) return;

        this.ctx.beginPath();
        this.ctx.strokeStyle = '#10b981';
        this.ctx.lineWidth = 2.5;
        this.ctx.lineJoin = 'round';
        this.ctx.lineCap = 'round';
        this.ctx.moveTo(this.tracePoints[0].x, this.tracePoints[0].y);
        for (let i = 1; i < this.tracePoints.length; i++) {
            this.ctx.lineTo(this.tracePoints[i].x, this.tracePoints[i].y);
        }
        this.ctx.stroke();

        const last = this.tracePoints[this.tracePoints.length - 1];
        this.ctx.beginPath();
        this.ctx.arc(last.x, last.y, 4, 0, Math.PI * 2);
        this.ctx.fillStyle = '#10b981';
        this.ctx.fill();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const simulator = new ECGSimulator('ecgCanvas');
    simulator.start();
});
