"""
Arrhythmia Configuration Data.

Contains ECG parameters for each of the 54 arrhythmias.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple, List
from src.arrhythmias.types import ArrhythmiaType


@dataclass
class WaveformParams:
    """Parameters for a single ECG waveform component."""
    amplitude: float  # mV
    duration: float  # ms
    morphology: str  # 'normal', 'inverted', 'biphasic', 'absent', 'variable'
    
    
@dataclass
class ArrhythmiaConfig:
    """
    Complete configuration for an arrhythmia.
    
    Contains all parameters needed to generate realistic ECG.
    """
    # Identification
    name: str
    arrhythmia_type: ArrhythmiaType
    category: str  # 'supraventricular', 'ventricular', 'special'
    
    # Rate parameters
    rate_range: Tuple[int, int]  # (min, max) bpm
    rate_regularity: str  # 'regular', 'irregular', 'regularly_irregular'
    
    # Intervals (ms)
    pr_interval: Optional[Tuple[float, float]] = None  # (min, max) or None if absent
    qrs_duration: Tuple[float, float] = (80, 100)  # (min, max)
    qt_interval: Optional[Tuple[float, float]] = None
    
    # Wave parameters
    p_wave: WaveformParams = field(default_factory=lambda: WaveformParams(0.15, 80, 'normal'))
    qrs_complex: WaveformParams = field(default_factory=lambda: WaveformParams(1.0, 80, 'normal'))
    t_wave: WaveformParams = field(default_factory=lambda: WaveformParams(0.3, 160, 'normal'))
    
    # Special characteristics
    rhythm_pattern: str = 'regular'  # 'regular', 'irregular', 'patterned'
    conduction_ratio: Optional[str] = None  # e.g., '2:1', '3:1', 'variable'
    special_features: List[str] = field(default_factory=list)
    
    # Physiopathology
    mechanism: str = 'normal'  # 'automaticity', 'reentry', 'triggered', 'block'
    origin: str = 'sinus'  # 'sinus', 'atrial', 'junctional', 'ventricular'
    
    # Clinical
    is_life_threatening: bool = False
    urgency: str = 'low'  # 'low', 'medium', 'high', 'critical'
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'type': self.arrhythmia_type.value,
            'category': self.category,
            'rate_range': self.rate_range,
            'rate_regularity': self.rate_regularity,
            'pr_interval': self.pr_interval,
            'qrs_duration': self.qrs_duration,
            'mechanism': self.mechanism,
            'origin': self.origin,
            'is_life_threatening': self.is_life_threatening,
            'urgency': self.urgency
        }


# ========================================
# ARRHYTHMIA CONFIGURATIONS DATABASE
# ========================================

ARRHYTHMIA_CONFIGS: Dict[ArrhythmiaType, ArrhythmiaConfig] = {
    
    # ========================================
    # NORMAL SINUS RHYTHM (baseline)
    # ========================================
    ArrhythmiaType.NORMAL_SINUS: ArrhythmiaConfig(
        name="Normal Sinus Rhythm",
        arrhythmia_type=ArrhythmiaType.NORMAL_SINUS,
        category="normal",
        rate_range=(60, 100),
        rate_regularity="regular",
        pr_interval=(120, 200),
        qrs_duration=(80, 100),
        qt_interval=(350, 440),
        p_wave=WaveformParams(0.15, 80, 'normal'),
        qrs_complex=WaveformParams(1.0, 80, 'normal'),
        t_wave=WaveformParams(0.3, 160, 'normal'),
        mechanism="normal",
        origin="sinus",
        is_life_threatening=False,
        urgency="low"
    ),
    
    # ========================================
    # SUPRAVENTRICULAR BRADYARRHYTHMIAS
    # ========================================
    ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA: ArrhythmiaConfig(
        name="Sinus Bradycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA,
        category="supraventricular",
        rate_range=(30, 59),
        rate_regularity="regular",
        pr_interval=(120, 200),
        qrs_duration=(80, 100),
        p_wave=WaveformParams(0.15, 80, 'normal'),
        qrs_complex=WaveformParams(1.0, 80, 'normal'),
        t_wave=WaveformParams(0.3, 160, 'normal'),
        mechanism="automaticity",
        origin="sinus",
        special_features=["Normal P waves", "1:1 AV conduction"],
        is_life_threatening=False,
        urgency="low"
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_1: ArrhythmiaConfig(
        name="First Degree AV Block",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_1,
        category="supraventricular",
        rate_range=(40, 100),
        rate_regularity="regular",
        pr_interval=(210, 400),
        qrs_duration=(80, 100),
        p_wave=WaveformParams(0.15, 80, 'normal'),
        qrs_complex=WaveformParams(1.0, 80, 'normal'),
        mechanism="block",
        origin="sinus",
        special_features=["Prolonged PR interval", "All P waves conducted"],
        is_life_threatening=False,
        urgency="low"
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH: ArrhythmiaConfig(
        name="Second Degree AV Block Type I (Wenckebach)",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH,
        category="supraventricular",
        rate_range=(40, 80),
        rate_regularity="regularly_irregular",
        pr_interval=(200, 400),
        qrs_duration=(80, 100),
        rhythm_pattern="patterned",
        conduction_ratio="variable",
        mechanism="block",
        origin="sinus",
        special_features=["Progressive PR prolongation", "Dropped beats", "Grouped beating"],
        is_life_threatening=False,
        urgency="medium"
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_MOBITZ: ArrhythmiaConfig(
        name="Second Degree AV Block Type II (Mobitz II)",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_MOBITZ,
        category="supraventricular",
        rate_range=(30, 70),
        rate_regularity="regularly_irregular",
        pr_interval=(120, 200),
        qrs_duration=(100, 140),
        conduction_ratio="variable",
        mechanism="block",
        origin="sinus",
        special_features=["Fixed PR before dropped beat", "Wide QRS", "Can progress to complete block"],
        is_life_threatening=True,
        urgency="high"
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3: ArrhythmiaConfig(
        name="Third Degree (Complete) AV Block",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3,
        category="supraventricular",
        rate_range=(20, 50),
        rate_regularity="regular",
        pr_interval=None,
        qrs_duration=(80, 160),
        mechanism="block",
        origin="ventricular",
        special_features=["AV dissociation", "Independent P waves", "Escape rhythm"],
        is_life_threatening=True,
        urgency="critical"
    ),
    
    # ========================================
    # SUPRAVENTRICULAR TACHYARRHYTHMIAS
    # ========================================
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION: ArrhythmiaConfig(
        name="Atrial Fibrillation",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
        category="supraventricular",
        rate_range=(60, 180),
        rate_regularity="irregular",
        pr_interval=None,
        qrs_duration=(80, 100),
        p_wave=WaveformParams(0, 0, 'absent'),
        rhythm_pattern="irregular",
        mechanism="reentry",
        origin="atrial",
        special_features=["No P waves", "Fibrillatory baseline", "Irregularly irregular RR"],
        is_life_threatening=False,
        urgency="medium"
    ),
    
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER: ArrhythmiaConfig(
        name="Atrial Flutter",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER,
        category="supraventricular",
        rate_range=(130, 150),  # Ventricular rate with 2:1 block
        rate_regularity="regular",
        pr_interval=None,
        qrs_duration=(80, 100),
        conduction_ratio="2:1",
        mechanism="reentry",
        origin="atrial",
        special_features=["Sawtooth pattern", "Flutter waves ~300/min", "Regular AV conduction ratio"],
        is_life_threatening=False,
        urgency="medium"
    ),
    
    ArrhythmiaType.SUPRA_TACHY_AVNRT: ArrhythmiaConfig(
        name="AV Nodal Reentrant Tachycardia (AVNRT)",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_AVNRT,
        category="supraventricular",
        rate_range=(140, 220),
        rate_regularity="regular",
        pr_interval=(80, 120),
        qrs_duration=(80, 100),
        mechanism="reentry",
        origin="junctional",
        special_features=["Pseudo-R' in V1", "Pseudo-S in inferior leads", "P waves hidden in QRS"],
        is_life_threatening=False,
        urgency="medium"
    ),
    
    ArrhythmiaType.SUPRA_TACHY_WPW: ArrhythmiaConfig(
        name="Wolff-Parkinson-White Syndrome",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_WPW,
        category="supraventricular",
        rate_range=(140, 250),
        rate_regularity="regular",
        pr_interval=(80, 120),
        qrs_duration=(100, 160),
        mechanism="reentry",
        origin="atrial",
        special_features=["Delta wave", "Short PR", "Wide QRS", "Accessory pathway"],
        is_life_threatening=True,
        urgency="high"
    ),
    
    # ========================================
    # VENTRICULAR ARRHYTHMIAS
    # ========================================
    ArrhythmiaType.VENT_PVC: ArrhythmiaConfig(
        name="Premature Ventricular Contraction (PVC)",
        arrhythmia_type=ArrhythmiaType.VENT_PVC,
        category="ventricular",
        rate_range=(60, 100),  # Base rhythm
        rate_regularity="irregular",
        qrs_duration=(120, 200),
        mechanism="automaticity",
        origin="ventricular",
        special_features=["Wide QRS", "No preceding P", "Compensatory pause", "T wave opposite QRS"],
        is_life_threatening=False,
        urgency="low"
    ),
    
    ArrhythmiaType.VENT_VT_MONO: ArrhythmiaConfig(
        name="Monomorphic Ventricular Tachycardia",
        arrhythmia_type=ArrhythmiaType.VENT_VT_MONO,
        category="ventricular",
        rate_range=(100, 250),
        rate_regularity="regular",
        qrs_duration=(120, 200),
        p_wave=WaveformParams(0, 0, 'absent'),
        mechanism="reentry",
        origin="ventricular",
        special_features=["Wide QRS", "Uniform morphology", "AV dissociation"],
        is_life_threatening=True,
        urgency="critical"
    ),
    
    ArrhythmiaType.VENT_TORSADES: ArrhythmiaConfig(
        name="Torsades de Pointes",
        arrhythmia_type=ArrhythmiaType.VENT_TORSADES,
        category="ventricular",
        rate_range=(200, 300),
        rate_regularity="irregular",
        qrs_duration=(120, 200),
        mechanism="triggered",
        origin="ventricular",
        special_features=["Twisting QRS axis", "Associated with long QT", "Polymorphic"],
        is_life_threatening=True,
        urgency="critical"
    ),
    
    ArrhythmiaType.VENT_VF_COARSE: ArrhythmiaConfig(
        name="Ventricular Fibrillation (Coarse)",
        arrhythmia_type=ArrhythmiaType.VENT_VF_COARSE,
        category="ventricular",
        rate_range=(300, 500),
        rate_regularity="irregular",
        qrs_duration=None,
        p_wave=WaveformParams(0, 0, 'absent'),
        mechanism="reentry",
        origin="ventricular",
        special_features=["No organized QRS", "Chaotic rhythm", "Amplitude > 3mm"],
        is_life_threatening=True,
        urgency="critical"
    ),
    
    ArrhythmiaType.VENT_VF_FINE: ArrhythmiaConfig(
        name="Ventricular Fibrillation (Fine)",
        arrhythmia_type=ArrhythmiaType.VENT_VF_FINE,
        category="ventricular",
        rate_range=(300, 500),
        rate_regularity="irregular",
        qrs_duration=None,
        mechanism="reentry",
        origin="ventricular",
        special_features=["Low amplitude fibrillation", "< 3mm amplitude", "May resemble asystole"],
        is_life_threatening=True,
        urgency="critical"
    ),
    
    ArrhythmiaType.VENT_ASYSTOLE: ArrhythmiaConfig(
        name="Asystole",
        arrhythmia_type=ArrhythmiaType.VENT_ASYSTOLE,
        category="ventricular",
        rate_range=(0, 0),
        rate_regularity="regular",
        qrs_duration=None,
        p_wave=WaveformParams(0, 0, 'absent'),
        mechanism="block",
        origin="none",
        special_features=["Flat line", "No electrical activity"],
        is_life_threatening=True,
        urgency="critical"
    ),
}


def get_arrhythmia_config(arrhythmia: ArrhythmiaType) -> ArrhythmiaConfig:
    """
    Get configuration for an arrhythmia.
    
    Args:
        arrhythmia: The arrhythmia type
        
    Returns:
        ArrhythmiaConfig object with all parameters
        
    Raises:
        ValueError: If arrhythmia not found in database
    """
    if arrhythmia in ARRHYTHMIA_CONFIGS:
        return ARRHYTHMIA_CONFIGS[arrhythmia]
    
    # Return default config for arrhythmias not yet fully configured
    return ArrhythmiaConfig(
        name=arrhythmia.value.replace('_', ' ').title(),
        arrhythmia_type=arrhythmia,
        category="unknown",
        rate_range=(60, 100),
        rate_regularity="regular",
        mechanism="unknown",
        origin="unknown"
    )
