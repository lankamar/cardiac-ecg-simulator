/**
 * 🫀 ECG Simulator - Educational Mode with Realistic Layer
 * 
 * Three simulation levels:
 * - SIMPLE: Lookup tables (<1ms) - Educational
 * - INTERMEDIATE: Parametric models (~100ms) - Clinical
 * - REALISTIC: Hodgkin-Huxley (seconds) - Research
 */

// =============================================================================
// EDUCATIONAL DATA FOR EACH ARRHYTHMIA
// =============================================================================

const ARRHYTHMIA_EDUCATION = {
    normal_sinus: {
        features: [
            "Onda P positiva en DII antes de cada QRS",
            "Intervalo PR constante (120-200ms = 3-5 cuadros pequeños)",
            "QRS estrecho (<120ms = <3 cuadros pequeños)",
            "Ritmo regular: RR constante",
            "Frecuencia 60-100 lpm"
        ],
        mechanism: "Automatismo normal del nodo sinusal. El impulso se origina en el nodo SA, despolariza las aurículas (onda P), pasa por el nodo AV con retraso fisiológico (intervalo PR), y despolariza los ventrículos (QRS).",
        alert: null
    },
    sinus_bradycardia: {
        features: [
            "Todo normal EXCEPTO frecuencia <60 lpm",
            "Onda P presente, PR normal",
            "QRS estrecho",
            "RR prolongado (>1 segundo = >5 cuadros grandes)"
        ],
        mechanism: "Automatismo sinusal disminuido. Puede ser fisiológico (atletas, sueño) o patológico (hipotiroidismo, fármacos).",
        alert: null
    },
    av_block_1: {
        features: [
            "PR PROLONGADO >200ms (>5 cuadros pequeños)",
            "Cada P conduce un QRS",
            "PR constante en cada latido",
            "¡Contar los cuadros del PR!"
        ],
        mechanism: "Retraso en la conducción AV. El impulso pasa pero tarda más de lo normal. Suele ser en el nodo AV.",
        alert: null
    },
    av_block_2_wenckebach: {
        features: [
            "PR se ALARGA progresivamente latido a latido",
            "Hasta que una P NO conduce (QRS ausente)",
            "Patrón cíclico: PR corto → más largo → más largo → P bloqueada",
            "Medir PR en cada ciclo: va aumentando"
        ],
        mechanism: "Mobitz I / Wenckebach: Fatiga progresiva del nodo AV. Cada impulso llega cuando el nodo aún está recuperándose del anterior.",
        alert: "Puede progresar a bloqueo completo. Monitorizar."
    },
    av_block_2_mobitz: {
        features: [
            "PR CONSTANTE (no cambia)",
            "Súbitamente una P no conduce (QRS ausente)",
            "QRS puede ser ancho (infranodal)",
            "Patrón puede ser 2:1, 3:1, etc."
        ],
        mechanism: "Mobitz II: Bloqueo intermitente infranodal (His-Purkinje). El PR antes del bloqueo es igual al PR después.",
        alert: "⚠️ ALTO RIESGO de progresar a bloqueo completo. Puede requerir marcapasos."
    },
    av_block_complete: {
        features: [
            "P y QRS completamente DISOCIADOS",
            "Las P tienen su ritmo (más rápido)",
            "Los QRS tienen su ritmo (más lento, 30-45 lpm)",
            "PR variable (no hay relación)",
            "QRS ancho si escape ventricular"
        ],
        mechanism: "Bloqueo AV completo: Ningún impulso auricular llega a los ventrículos. El ritmo ventricular depende de un marcapasos de escape (nodal o ventricular).",
        alert: "⚠️ CRÍTICO: Puede causar síncope, muerte súbita. Requiere marcapasos."
    },
    atrial_fibrillation: {
        features: [
            "NO hay ondas P - línea de base fibrilatoria irregular",
            "QRS estrecho pero TOTALMENTE IRREGULAR",
            "RR completamente variable (medir 3-4 RR distintos)",
            "Frecuencia ventricular variable"
        ],
        mechanism: "Múltiples circuitos de reentrada en las aurículas (>300/min). Solo algunos impulsos conducen aleatoriamente a los ventrículos.",
        alert: "Riesgo de tromboembolismo. Requiere anticoagulación si >48h."
    },
    atrial_flutter: {
        features: [
            "Ondas F en dientes de sierra (~300/min)",
            "Patrón más visible en DII, DIII, aVF",
            "Conducción típica 2:1 (150 lpm), 4:1 (75 lpm)",
            "QRS regular (a diferencia de FA)"
        ],
        mechanism: "Macro-reentrada auricular (típico: circuito en aurícula derecha alrededor del istmo cavotricuspídeo). Frecuencia auricular ~300.",
        alert: "También tiene riesgo tromboembólico."
    },
    wpw: {
        features: [
            "PR CORTO (<120ms = <3 cuadros pequeños)",
            "Onda DELTA: empastamiento inicial del QRS",
            "QRS ANCHO por preexcitación",
            "Buscar delta wave al inicio del QRS"
        ],
        mechanism: "Vía accesoria (haz de Kent) que conecta aurícula y ventrículo saltando el nodo AV. Preexcitación ventricular.",
        alert: "⚠️ En FA puede conducir muy rápido por la vía accesoria. Riesgo de FV."
    },
    pvc: {
        features: [
            "QRS ANCHO y diferente (>120ms = >3 cuadros)",
            "No precedido por onda P",
            "Pausa compensadora completa",
            "Onda T en dirección opuesta al QRS"
        ],
        mechanism: "Foco ectópico ventricular que dispara antes de lo esperado. La despolarización anormal produce QRS ancho y morfología diferente.",
        alert: null
    },
    pvc_bigeminy: {
        features: [
            "Patrón 1:1 - Un latido normal, un PVC",
            "Alternancia regular",
            "Los PVC son anchos y diferentes",
            "Puede reducir gasto cardíaco efectivo"
        ],
        mechanism: "PVC que ocurre en patrón bigeminado. Puede indicar irritabilidad ventricular aumentada.",
        alert: "Monitorizar por posible progresión a VT."
    },
    vt_mono: {
        features: [
            "QRS ANCHO (>120ms) y todos IGUALES",
            "Frecuencia >100 lpm (típico 140-220)",
            "Sin P visibles (o disociadas)",
            "Ritmo regular",
            "Medir QRS: >3 cuadros pequeños"
        ],
        mechanism: "Reentrada ventricular o foco automático. Morfología uniforme indica origen único.",
        alert: "⚠️ CRÍTICO: Puede degenerar en FV. Requiere cardioversión si inestable."
    },
    vt_poly: {
        features: [
            "QRS ancho pero CAMBIAN DE FORMA",
            "Cada QRS tiene morfología diferente",
            "Muy irregular",
            "Frecuencia alta variable"
        ],
        mechanism: "Múltiples focos ventriculares o isquemia activa. Los QRS cambiantes reflejan vectores de despolarización cambiantes.",
        alert: "⚠️ MUY CRÍTICO: Alto riesgo de FV. ¿Isquemia? ¿QT largo?"
    },
    torsades: {
        features: [
            "Los QRS parecen GIRAR alrededor de la línea de base",
            "Amplitud aumenta y disminuye cíclicamente",
            "Forma de 'torsión de puntas'",
            "Frecuencia 200-300 lpm"
        ],
        mechanism: "VT polimórfica asociada a QT largo. Post-despolarizaciones precoces por prolongación de repolarización.",
        alert: "⚠️ CRÍTICO: Tratar QT largo. Magnesio IV. Evitar antiarrítmicos clase I."
    },
    vf_coarse: {
        features: [
            "NO HAY QRS identificables",
            "Ondas caóticas de gran amplitud",
            "Frecuencia >300",
            "No hay gasto cardíaco efectivo"
        ],
        mechanism: "Actividad eléctrica ventricular completamente caótica. Múltiples frentes de onda sin coordinación.",
        alert: "⚠️⚠️ PARO CARDÍACO - DESFIBRILAR INMEDIATAMENTE"
    },
    vf_fine: {
        features: [
            "Similar a VF gruesa pero BAJA AMPLITUD",
            "Ondas pequeñas e irregulares",
            "Puede parecer casi asistolia",
            "Refleja miocardio isquémico/agotado"
        ],
        mechanism: "VF de larga duración o en corazón muy dañado. Menor masa miocárdica capaz de despolarizarse.",
        alert: "⚠️⚠️ PARO CARDÍACO - RCP + Adrenalina + Desfibrilar"
    },
    asystole: {
        features: [
            "LÍNEA PLANA",
            "No hay actividad eléctrica ventricular",
            "Puede haber ondas P (actividad auricular)",
            "Verificar en dos derivaciones"
        ],
        mechanism: "Ausencia de actividad eléctrica ventricular. Puede ser el estadío final de cualquier paro cardíaco.",
        alert: "⚠️⚠️ PARO CARDÍACO - RCP + Adrenalina. NO desfibrilar."
    },
    brugada: {
        features: [
            "Elevación ST coved (tipo 1) en V1-V2",
            "Patrón de silla de montar o coved",
            "Bloqueo de rama derecha incompleto",
            "QRS puede estar prolongado en precordiales derechas"
        ],
        mechanism: "Canalopatía de sodio (SCN5A). Predispone a VF y muerte súbita, especialmente en reposo o sueño.",
        alert: "⚠️ ALTO RIESGO de muerte súbita. Evaluar para DAI."
    }
};

// Fill in missing arrhythmias with default education
const defaultEducation = {
    features: ["Analizar ritmo", "Medir intervalos", "Evaluar morfología QRS", "Identificar ondas P"],
    mechanism: "Consultar características específicas de esta arritmia.",
    alert: null
};

// =============================================================================
// COMPLETE 54 ARRHYTHMIA CONFIGURATIONS
// =============================================================================

const ARRHYTHMIAS = {
    // Normal
    normal_sinus: {
        name: "Normal Sinus Rhythm", rate: [60, 100],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Normal Automaticity', urgency: 'low'
    },

    // Brady
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
        name: "AV Block 1st Degree", rate: [50, 90],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 300, regularity: 'regular', baseline: 'flat',
        mechanism: 'Conduction Delay', urgency: 'low'
    },
    av_block_2_wenckebach: {
        name: "AV Block 2nd Wenckebach", rate: [50, 80],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 200, regularity: 'irregular', baseline: 'flat', pattern: 'wenckebach',
        wenckebachCycle: 4, prProgression: [200, 280, 360, 0],
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

    // SVT Tachy
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
        hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flutter', flutterRate: 300,
        mechanism: 'Macro-Reentry', urgency: 'medium'
    },
    atrial_flutter_atypical: {
        name: "Atypical Flutter", rate: [120, 200],
        hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flutter', flutterRate: 250,
        mechanism: 'Atypical Reentry', urgency: 'medium'
    },
    atrial_fibrillation: {
        name: "Atrial Fibrillation", rate: [60, 160],
        hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 0, regularity: 'chaotic', baseline: 'fibrillatory',
        mechanism: 'Multiple Reentry', urgency: 'medium'
    },
    avnrt: {
        name: "AVNRT", rate: [140, 220],
        hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 80, regularity: 'regular', baseline: 'flat',
        mechanism: 'Nodal Reentry', urgency: 'medium'
    },
    avrt: {
        name: "AVRT", rate: [140, 250],
        hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
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
        hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25,
        prInterval: 0, regularity: 'regular', baseline: 'flat',
        mechanism: 'Reentry', urgency: 'medium'
    },
    mat: {
        name: "MAT", rate: [100, 180],
        hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'mat',
        mechanism: 'Multiple Foci', urgency: 'medium'
    },
    focal_at: {
        name: "Focal AT", rate: [150, 250],
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
        name: "Ectopic Atrial", rate: [60, 100],
        hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3,
        prInterval: 160, regularity: 'regular', baseline: 'flat',
        mechanism: 'Ectopic Pacemaker', urgency: 'low'
    },

    // Other SVT
    pac: { name: "PAC", rate: [60, 100], hasP: true, pAmp: 0.12, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'pac', mechanism: 'Premature Beat', urgency: 'low' },
    pjc: { name: "PJC", rate: [60, 100], hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'pjc', mechanism: 'Junctional Ectopy', urgency: 'low' },
    junctional_escape: { name: "Junctional Escape", rate: [40, 60], hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Escape Rhythm', urgency: 'medium' },
    junctional_tachy: { name: "Junctional Tachy", rate: [70, 130], hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Enhanced Automaticity', urgency: 'medium' },
    jet: { name: "JET", rate: [120, 200], hasP: false, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.25, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Ectopic Junction', urgency: 'high' },
    wandering_pacemaker: { name: "Wandering Pacemaker", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'wandering', mechanism: 'Variable Focus', urgency: 'low' },
    sinus_arrhythmia: { name: "Sinus Arrhythmia", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', mechanism: 'Respiratory Variation', urgency: 'low' },
    sinus_pause: { name: "Sinus Pause", rate: [50, 80], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'pause', mechanism: 'Transient Arrest', urgency: 'medium' },
    sinus_arrest: { name: "Sinus Arrest", rate: [30, 60], hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'arrest', mechanism: 'Prolonged Arrest', urgency: 'high' },
    sinoatrial_block: { name: "SA Exit Block", rate: [50, 80], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'sa_block', mechanism: 'Exit Block', urgency: 'medium' },

    // Ventricular
    pvc: { name: "PVC", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'pvc', pvcRate: 6, mechanism: 'Ectopic Focus', urgency: 'low' },
    pvc_bigeminy: { name: "PVC Bigeminy", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'bigeminy', mechanism: 'Alternating Ectopy', urgency: 'medium' },
    pvc_trigeminy: { name: "PVC Trigeminy", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'trigeminy', mechanism: 'Patterned Ectopy', urgency: 'medium' },
    pvc_couplet: { name: "PVC Couplet", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'couplet', mechanism: 'Paired Ectopy', urgency: 'medium' },
    pvc_triplet: { name: "PVC Triplet", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'triplet', mechanism: 'Brief VT', urgency: 'high' },
    aivr: { name: "AIVR", rate: [40, 110], hasP: false, qrsDuration: 140, qrsAmp: 1.3, tAmp: 0.4, tPolarity: -1, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Accelerated Escape', urgency: 'low' },
    ventricular_escape: { name: "Ventricular Escape", rate: [20, 40], hasP: false, qrsDuration: 160, qrsAmp: 1.5, tAmp: 0.5, tPolarity: -1, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Ventricular Escape', urgency: 'high' },
    vt_mono: { name: "VT Monomorphic", rate: [140, 220], hasP: false, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Ventricular Reentry', urgency: 'critical' },
    vt_poly: { name: "VT Polymorphic", rate: [100, 250], hasP: false, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0, prInterval: 0, regularity: 'irregular', baseline: 'flat', pattern: 'polymorphic', mechanism: 'Multiple Reentry', urgency: 'critical' },
    vt_sustained: { name: "VT Sustained", rate: [100, 250], hasP: false, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Sustained Reentry', urgency: 'critical' },
    vt_nonsustained: { name: "NSVT", rate: [100, 250], hasP: false, qrsDuration: 140, qrsAmp: 1.5, tAmp: 0.4, tPolarity: -1, prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'nsvt', mechanism: 'Brief VT', urgency: 'high' },
    torsades: { name: "Torsades de Pointes", rate: [200, 300], hasP: false, qrsDuration: 150, qrsAmp: 1.2, tAmp: 0, prInterval: 0, regularity: 'irregular', baseline: 'torsades', mechanism: 'Triggered Activity', urgency: 'critical' },
    vf_coarse: { name: "VF Coarse", rate: [300, 500], hasP: false, qrsDuration: 0, qrsAmp: 0.8, tAmp: 0, prInterval: 0, regularity: 'chaotic', baseline: 'vf_coarse', mechanism: 'Chaotic Reentry', urgency: 'critical' },
    vf_fine: { name: "VF Fine", rate: [300, 500], hasP: false, qrsDuration: 0, qrsAmp: 0.3, tAmp: 0, prInterval: 0, regularity: 'chaotic', baseline: 'vf_fine', mechanism: 'Chaotic Reentry', urgency: 'critical' },
    asystole: { name: "Asystole", rate: [0, 0], hasP: false, qrsDuration: 0, qrsAmp: 0, tAmp: 0, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'No Activity', urgency: 'critical' },
    idioventricular: { name: "Idioventricular", rate: [20, 40], hasP: false, qrsDuration: 160, qrsAmp: 1.5, tAmp: 0.5, tPolarity: -1, prInterval: 0, regularity: 'regular', baseline: 'flat', mechanism: 'Ventricular Escape', urgency: 'high' },

    // Special
    parasystole: { name: "Parasystole", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'parasystole', mechanism: 'Protected Focus', urgency: 'low' },
    fusion: { name: "Fusion Beat", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.2, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'fusion', mechanism: 'Dual Activation', urgency: 'low' },
    capture: { name: "Capture Beat", rate: [140, 200], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'capture', mechanism: 'SVT Capture', urgency: 'low' },
    r_on_t: { name: "R-on-T", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'r_on_t', mechanism: 'Vulnerable Period', urgency: 'critical' },
    ashman: { name: "Ashman", rate: [80, 140], hasP: true, pAmp: 0.15, qrsDuration: 120, qrsAmp: 1.2, tAmp: 0.3, prInterval: 160, regularity: 'irregular', baseline: 'flat', pattern: 'ashman', mechanism: 'Aberrant Conduction', urgency: 'low' },
    concealed: { name: "Concealed Conduction", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 80, qrsAmp: 1.0, tAmp: 0.3, prInterval: 180, regularity: 'irregular', baseline: 'flat', pattern: 'concealed', mechanism: 'Hidden Conduction', urgency: 'low' },
    av_dissociation: { name: "AV Dissociation", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.2, tAmp: 0.3, prInterval: 0, regularity: 'regular', baseline: 'flat', pattern: 'dissociation', mechanism: 'Independent Rhythms', urgency: 'medium' },
    brugada: { name: "Brugada Pattern", rate: [60, 100], hasP: true, pAmp: 0.15, qrsDuration: 100, qrsAmp: 1.0, tAmp: 0.2, tPolarity: -1, prInterval: 160, regularity: 'regular', baseline: 'flat', pattern: 'brugada', mechanism: 'Channelopathy', urgency: 'high' }
};

console.log(`🫀 Loaded ${Object.keys(ARRHYTHMIAS).length} arrhythmias`);

// =============================================================================
// HODGKIN-HUXLEY MODEL (REALISTIC LAYER)
// =============================================================================

class HodgkinHuxleyModel {
    constructor(dt = 0.1) {
        this.dt = dt; // time step in ms
        this.C_m = 1.0;  // membrane capacitance (µF/cm²)

        // Conductances (mS/cm²)
        this.g_Na = 120.0;
        this.g_K = 36.0;
        this.g_L = 0.3;

        // Reversal potentials (mV)
        this.E_Na = 50.0;
        this.E_K = -77.0;
        this.E_L = -54.4;

        this.V_rest = -65.0;
        this.reset();
    }

    reset() {
        this.V = this.V_rest;
        this.m = this._m_inf(this.V_rest);
        this.h = this._h_inf(this.V_rest);
        this.n = this._n_inf(this.V_rest);
    }

    _alpha_m(V) { return Math.abs(V + 40) < 1e-6 ? 1.0 : 0.1 * (V + 40) / (1 - Math.exp(-(V + 40) / 10)); }
    _beta_m(V) { return 4.0 * Math.exp(-(V + 65) / 18); }
    _alpha_h(V) { return 0.07 * Math.exp(-(V + 65) / 20); }
    _beta_h(V) { return 1.0 / (1 + Math.exp(-(V + 35) / 10)); }
    _alpha_n(V) { return Math.abs(V + 55) < 1e-6 ? 0.1 : 0.01 * (V + 55) / (1 - Math.exp(-(V + 55) / 10)); }
    _beta_n(V) { return 0.125 * Math.exp(-(V + 65) / 80); }

    _m_inf(V) { return this._alpha_m(V) / (this._alpha_m(V) + this._beta_m(V)); }
    _h_inf(V) { return this._alpha_h(V) / (this._alpha_h(V) + this._beta_h(V)); }
    _n_inf(V) { return this._alpha_n(V) / (this._alpha_n(V) + this._beta_n(V)); }
    _tau_m(V) { return 1.0 / (this._alpha_m(V) + this._beta_m(V)); }
    _tau_h(V) { return 1.0 / (this._alpha_h(V) + this._beta_h(V)); }
    _tau_n(V) { return 1.0 / (this._alpha_n(V) + this._beta_n(V)); }

    I_Na() { return this.g_Na * Math.pow(this.m, 3) * this.h * (this.V - this.E_Na); }
    I_K() { return this.g_K * Math.pow(this.n, 4) * (this.V - this.E_K); }
    I_L() { return this.g_L * (this.V - this.E_L); }
    I_ion() { return this.I_Na() + this.I_K() + this.I_L(); }

    step(I_stim = 0) {
        const I_total = this.I_ion();
        const dV = (I_stim - I_total) / this.C_m;
        this.V += dV * this.dt;

        this.m += (this._m_inf(this.V) - this.m) / this._tau_m(this.V) * this.dt;
        this.h += (this._h_inf(this.V) - this.h) / this._tau_h(this.V) * this.dt;
        this.n += (this._n_inf(this.V) - this.n) / this._tau_n(this.V) * this.dt;

        this.m = Math.max(0, Math.min(1, this.m));
        this.h = Math.max(0, Math.min(1, this.h));
        this.n = Math.max(0, Math.min(1, this.n));

        return this.V;
    }

    simulateAP(duration_ms = 400, stim_start = 10, stim_dur = 2, stim_amp = 20) {
        this.reset();
        const n_steps = Math.floor(duration_ms / this.dt);
        const V_trace = [];

        for (let i = 0; i < n_steps; i++) {
            const t = i * this.dt;
            const I_stim = (t >= stim_start && t < stim_start + stim_dur) ? stim_amp : 0;
            V_trace.push(this.step(I_stim));
        }
        return V_trace;
    }
}

// =============================================================================
// ECG SIMULATOR CLASS
// =============================================================================

class ECGSimulator {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.isRunning = false;
        this.currentArrhythmia = ARRHYTHMIAS.normal_sinus;
        this.currentKey = 'normal_sinus';
        this.heartRate = 75;
        this.noiseLevel = 0;
        this.speed = 25;
        this.lead = 'II';
        this.layer = 'simple'; // simple, intermediate, realistic
        this.beatCount = 0;
        this.tracePoints = [];
        this.maxPoints = 3000;
        this.drawX = 0;
        this.sampleBuffer = [];
        this.sampleIndex = 0;

        // Hodgkin-Huxley for realistic layer
        this.hhModel = new HodgkinHuxleyModel(0.1);

        this.setupCanvas();
        this.setupEventListeners();
        this.updateEducationalPanel();
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
        // Layer selector
        document.querySelectorAll('.layer-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.layer-btn').forEach(b => b.classList.remove('active'));
                e.target.closest('.layer-btn').classList.add('active');
                this.layer = e.target.closest('.layer-btn').dataset.layer;
                this.updateLayerInfo();
                this.sampleBuffer = [];
                this.sampleIndex = 0;
            });
        });

        document.getElementById('arrhythmiaSelect').addEventListener('change', (e) => {
            this.setArrhythmia(e.target.value);
        });

        document.getElementById('hrSlider').addEventListener('input', (e) => {
            this.heartRate = parseInt(e.target.value);
            document.getElementById('hrValue').textContent = `${this.heartRate} bpm`;
            this.updateEducationalPanel();
        });

        document.getElementById('noiseSlider').addEventListener('input', (e) => {
            this.noiseLevel = parseInt(e.target.value) / 100;
            document.getElementById('noiseValue').textContent = `${e.target.value}%`;
        });

        document.getElementById('speedSlider').addEventListener('input', (e) => {
            this.speed = parseInt(e.target.value);
            document.getElementById('speedValue').textContent = `${e.target.value} mm/s`;
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

    updateLayerInfo() {
        const layerInfo = {
            simple: 'Lookup Tables',
            intermediate: 'Parametric Models',
            realistic: 'Hodgkin-Huxley'
        };
        document.getElementById('modelInfo').textContent = layerInfo[this.layer];
        document.getElementById('layerBadge').textContent = this.layer.toUpperCase();
    }

    setArrhythmia(key) {
        this.currentArrhythmia = ARRHYTHMIAS[key] || ARRHYTHMIAS.normal_sinus;
        this.currentKey = key;
        this.beatCount = 0;
        this.updateUI();
        this.updateEducationalPanel();
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
        document.getElementById('hrSlider').value = rate;
        document.getElementById('hrValue').textContent = `${rate} bpm`;
        this.heartRate = rate;
    }

    updateEducationalPanel() {
        const arr = this.currentArrhythmia;
        const edu = ARRHYTHMIA_EDUCATION[this.currentKey] || defaultEducation;
        const rate = this.heartRate;

        // Calculate intervals
        const pr = arr.prInterval || 0;
        const qrs = arr.qrsDuration || 80;
        const rr = rate > 0 ? Math.round(60000 / rate) : 0;
        const qt = pr + qrs + 200;

        // Update measurements with squares
        document.getElementById('eduPR').textContent = `${pr}ms`;
        document.getElementById('eduPRsq').textContent = `(${(pr / 40).toFixed(1)} cuadros)`;

        document.getElementById('eduQRS').textContent = `${qrs}ms`;
        document.getElementById('eduQRSsq').textContent = `(${(qrs / 40).toFixed(1)} cuadros)`;

        document.getElementById('eduQT').textContent = `${qt}ms`;
        document.getElementById('eduQTsq').textContent = `(${(qt / 40).toFixed(1)} cuadros)`;

        document.getElementById('eduRR').textContent = `${rr}ms`;
        document.getElementById('eduRRsq').textContent = `(${(rr / 40).toFixed(1)} cuadros)`;

        document.getElementById('eduHR').textContent = `${rate} bpm`;
        document.getElementById('eduHRcalc').textContent = rate > 0 ? `(1500/${Math.round(rr / 40)})` : '--';

        // Update key features
        const featuresEl = document.getElementById('keyFeatures');
        featuresEl.innerHTML = edu.features.map(f => `<li>${f}</li>`).join('');

        // Update mechanism
        document.getElementById('mechanismContent').textContent = edu.mechanism;

        // Update alert
        const alertBox = document.getElementById('alertBox');
        if (edu.alert) {
            alertBox.style.display = 'block';
            document.getElementById('alertContent').textContent = edu.alert;
        } else if (arr.urgency === 'critical') {
            alertBox.style.display = 'block';
            document.getElementById('alertContent').textContent = 'Arritmia crítica. Evaluar necesidad de intervención inmediata.';
        } else {
            alertBox.style.display = 'none';
        }
    }

    // Waveform generation methods (same as before)
    gaussian(x, mu, sigma) { return Math.exp(-Math.pow(x - mu, 2) / (2 * sigma * sigma)); }

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

    generateBeatSimple(arr, beatIndex) {
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

        for (let i = 0; i < totalSamples; i++) {
            const t = i / samplesPerMs;
            const cycleT = t / rrInterval;
            let y = 0;

            if (arr.baseline === 'fibrillatory') y += 0.03 * Math.sin(t * 0.05) + 0.02 * Math.sin(t * 0.13);
            else if (arr.baseline === 'flutter') {
                const fp = 60000 / (arr.flutterRate || 300);
                y += 0.15 * (2 * ((t % fp) / fp) - 1);
            }

            if (dropBeat && cycleT > 0.15) { samples.push(y); continue; }

            if (arr.hasP && !isPVC && cycleT >= 0 && cycleT < 0.08) {
                y += (arr.pAmp || 0.15) * this.gaussian(cycleT / 0.08, 0.5, 0.2);
            }

            const qrsStart = (prInterval || 160) / rrInterval;
            const qrsDuration = (isPVC ? 140 : arr.qrsDuration) / rrInterval;

            if (cycleT >= qrsStart && cycleT < qrsStart + qrsDuration) {
                const qrsT = (cycleT - qrsStart) / qrsDuration;
                y += (isPVC || arr.qrsDuration > 120) ? this.generateWideQRS(qrsT) : this.generateQRS(qrsT, arr);
            }

            const tStart = qrsStart + qrsDuration + 0.08;
            if ((arr.tAmp || 0) > 0 && cycleT >= tStart && cycleT < tStart + 0.15) {
                const tT = (cycleT - tStart) / 0.15;
                y += arr.tAmp * (isPVC ? -1 : (arr.tPolarity || 1)) * this.gaussian(tT, 0.5, 0.25);
            }

            samples.push(y);
        }
        return samples;
    }

    generateBeatRealistic(arr, beatIndex) {
        // Use Hodgkin-Huxley for action potential
        const rate = this.heartRate || 75;
        const rrInterval = 60000 / rate;

        // Generate action potential
        const apDuration = Math.min(400, rrInterval * 0.95);
        const ap = this.hhModel.simulateAP(apDuration, 10, 2, 25);

        // Convert AP to surface ECG (simplified)
        const samples = [];
        const samplesPerMs = 0.5;
        const targetSamples = Math.floor(rrInterval * samplesPerMs);

        // Resample and transform
        for (let i = 0; i < targetSamples; i++) {
            const apIndex = Math.floor(i / targetSamples * ap.length);
            const v = ap[apIndex] || -65;
            // Transform membrane potential to surface ECG
            const normalized = (v + 65) / 100; // Normalize to ~0-1
            samples.push(normalized * 0.8);
        }

        // Reset for next beat
        this.hhModel.reset();

        return samples;
    }

    generateVF(duration, coarse) {
        const samples = [];
        const amp = coarse ? 0.7 : 0.2;
        for (let i = 0; i < duration * 500; i++) {
            const t = i / 500;
            let y = amp * Math.sin(2 * Math.PI * 5 * t);
            y += amp * 0.7 * Math.sin(2 * Math.PI * 7 * t + 1);
            if (coarse) y *= 0.6 + 0.4 * Math.sin(2 * Math.PI * 0.5 * t);
            samples.push(y);
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

        if (arr.baseline === 'vf_coarse') { this.sampleBuffer = this.generateVF(2, true); return; }
        if (arr.baseline === 'vf_fine') { this.sampleBuffer = this.generateVF(2, false); return; }
        if (arr.baseline === 'torsades') { this.sampleBuffer = this.generateTorsades(2); return; }
        if (arr.rate[1] === 0) { this.sampleBuffer = new Array(1000).fill(0); return; }

        // Choose generator based on layer
        if (this.layer === 'realistic') {
            this.sampleBuffer = this.generateBeatRealistic(arr, this.beatCount);
        } else {
            this.sampleBuffer = this.generateBeatSimple(arr, this.beatCount);
        }
        this.beatCount++;
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
            this.drawX++;
            if (this.drawX > this.canvas.width) { this.drawX = 0; this.tracePoints = []; }
        }

        if (this.tracePoints.length > this.maxPoints) this.tracePoints = this.tracePoints.slice(-this.maxPoints);
        this.draw();
        requestAnimationFrame(() => this.animate());
    }

    draw() {
        this.ctx.fillStyle = 'rgba(26, 26, 26, 0.15)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        if (this.tracePoints.length < 2) return;

        this.ctx.beginPath();
        this.ctx.strokeStyle = this.layer === 'realistic' ? '#f59e0b' : '#10b981';
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
        this.ctx.fillStyle = this.layer === 'realistic' ? '#f59e0b' : '#10b981';
        this.ctx.fill();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const simulator = new ECGSimulator('ecgCanvas');
    simulator.start();
});
