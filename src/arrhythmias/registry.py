"""Arrhythmia Registry - Quick lookup for all 54 arrhythmias."""

from src.arrhythmias.types import ArrhythmiaType

# Complete registry with metadata
ARRHYTHMIA_REGISTRY = {
    # ========== SUPRAVENTRICULAR BRADYARRHYTHMIAS (6) ==========
    "sinus_bradycardia": {
        "type": ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA,
        "category": "supraventricular_brady",
        "rate": (30, 59),
        "qrs_width": "narrow",
        "mechanism": "decreased automaticity",
        "urgency": "low"
    },
    "sick_sinus_syndrome": {
        "type": ArrhythmiaType.SUPRA_BRADY_SICK_SINUS,
        "category": "supraventricular_brady",
        "rate": (30, 100),
        "qrs_width": "narrow",
        "mechanism": "sinus node dysfunction",
        "urgency": "medium"
    },
    "av_block_first_degree": {
        "type": ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_1,
        "category": "supraventricular_brady",
        "rate": (40, 100),
        "qrs_width": "narrow",
        "mechanism": "conduction delay",
        "urgency": "low"
    },
    "av_block_2_wenckebach": {
        "type": ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH,
        "category": "supraventricular_brady",
        "rate": (40, 80),
        "qrs_width": "narrow",
        "mechanism": "progressive block",
        "urgency": "medium"
    },
    "av_block_2_mobitz": {
        "type": ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_MOBITZ,
        "category": "supraventricular_brady",
        "rate": (30, 70),
        "qrs_width": "wide",
        "mechanism": "infranodal block",
        "urgency": "high"
    },
    "av_block_complete": {
        "type": ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3,
        "category": "supraventricular_brady",
        "rate": (20, 50),
        "qrs_width": "variable",
        "mechanism": "complete dissociation",
        "urgency": "critical"
    },
    
    # ========== SUPRAVENTRICULAR TACHYARRHYTHMIAS (14) ==========
    "sinus_tachycardia": {
        "type": ArrhythmiaType.SUPRA_TACHY_SINUS_TACHYCARDIA,
        "category": "supraventricular_tachy",
        "rate": (100, 180),
        "qrs_width": "narrow",
        "mechanism": "increased automaticity",
        "urgency": "low"
    },
    "atrial_fibrillation": {
        "type": ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
        "category": "supraventricular_tachy",
        "rate": (60, 180),
        "qrs_width": "narrow",
        "mechanism": "multiple reentry",
        "urgency": "medium"
    },
    "atrial_flutter": {
        "type": ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER,
        "category": "supraventricular_tachy",
        "rate": (130, 150),
        "qrs_width": "narrow",
        "mechanism": "macro-reentry",
        "urgency": "medium"
    },
    "avnrt": {
        "type": ArrhythmiaType.SUPRA_TACHY_AVNRT,
        "category": "supraventricular_tachy",
        "rate": (140, 220),
        "qrs_width": "narrow",
        "mechanism": "nodal reentry",
        "urgency": "medium"
    },
    "wpw_syndrome": {
        "type": ArrhythmiaType.SUPRA_TACHY_WPW,
        "category": "supraventricular_tachy",
        "rate": (140, 250),
        "qrs_width": "wide",
        "mechanism": "accessory pathway reentry",
        "urgency": "high"
    },
    
    # ========== VENTRICULAR ARRHYTHMIAS (16) ==========
    "pvc": {
        "type": ArrhythmiaType.VENT_PVC,
        "category": "ventricular",
        "rate": None,
        "qrs_width": "wide",
        "mechanism": "ectopic focus",
        "urgency": "low"
    },
    "ventricular_tachycardia_monomorphic": {
        "type": ArrhythmiaType.VENT_VT_MONO,
        "category": "ventricular",
        "rate": (100, 250),
        "qrs_width": "wide",
        "mechanism": "ventricular reentry",
        "urgency": "critical"
    },
    "torsades_de_pointes": {
        "type": ArrhythmiaType.VENT_TORSADES,
        "category": "ventricular",
        "rate": (200, 300),
        "qrs_width": "wide",
        "mechanism": "triggered activity",
        "urgency": "critical"
    },
    "ventricular_fibrillation_coarse": {
        "type": ArrhythmiaType.VENT_VF_COARSE,
        "category": "ventricular",
        "rate": (300, 500),
        "qrs_width": "none",
        "mechanism": "chaotic reentry",
        "urgency": "critical"
    },
    "ventricular_fibrillation_fine": {
        "type": ArrhythmiaType.VENT_VF_FINE,
        "category": "ventricular",
        "rate": (300, 500),
        "qrs_width": "none",
        "mechanism": "chaotic reentry",
        "urgency": "critical"
    },
    "asystole": {
        "type": ArrhythmiaType.VENT_ASYSTOLE,
        "category": "ventricular",
        "rate": 0,
        "qrs_width": "none",
        "mechanism": "no activity",
        "urgency": "critical"
    },
}
