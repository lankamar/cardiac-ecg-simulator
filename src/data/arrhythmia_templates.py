"""
ECG Arrhythmia Templates - Pre-computed waveform patterns.

Contains normalized ECG templates for fast lookup-based generation.
Each template defines the exact morphology for P, QRS, T waves and
their timing relationships.

Priority arrhythmias implemented:
1. Normal Sinus Rhythm (baseline)
2. Sinus Bradycardia
3. Sinus Tachycardia  
4. Atrial Fibrillation
5. Atrial Flutter
6. Ventricular Tachycardia (Monomorphic)
7. Ventricular Fibrillation
8. PVC (Premature Ventricular Contraction)
9. Complete AV Block (3rd degree)
10. Asystole
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Callable
import numpy as np
from enum import Enum

from src.arrhythmias.types import ArrhythmiaType


# =============================================================================
# TEMPLATE DATA STRUCTURES
# =============================================================================

@dataclass
class WaveTemplate:
    """Template for a single ECG wave component."""
    amplitude: float        # Peak amplitude in mV
    duration_ms: float      # Duration in milliseconds
    shape: str              # 'gaussian', 'triangle', 'sawtooth', 'sine', 'noise'
    polarity: int = 1       # 1 = positive, -1 = negative
    skew: float = 0.0       # Asymmetry factor (-1 to 1)
    
    def generate(self, sampling_rate: int = 500) -> np.ndarray:
        """Generate the wave samples."""
        samples = int(self.duration_ms * sampling_rate / 1000)
        if samples < 2:
            samples = 2
            
        if self.shape == 'gaussian':
            x = np.linspace(-3, 3, samples)
            wave = np.exp(-x**2)
        elif self.shape == 'triangle':
            half = samples // 2
            wave = np.concatenate([
                np.linspace(0, 1, half),
                np.linspace(1, 0, samples - half)
            ])
        elif self.shape == 'sawtooth':
            wave = np.linspace(1, -1, samples)
        elif self.shape == 'sine':
            wave = np.sin(np.linspace(0, np.pi, samples))
        elif self.shape == 'noise':
            wave = np.random.randn(samples) * 0.5
        elif self.shape == 'qrs':
            # Specific QRS morphology: Q-R-S pattern
            q_len = samples // 5
            r_len = samples // 3
            s_len = samples - q_len - r_len
            q = -0.15 * np.sin(np.linspace(0, np.pi, q_len))
            r = np.sin(np.linspace(0, np.pi, r_len))
            s = -0.3 * np.sin(np.linspace(0, np.pi, s_len))
            wave = np.concatenate([q, r, s])
        elif self.shape == 'wide_qrs':
            # Wide QRS for ventricular arrhythmias
            samples = int(samples * 1.5)  # Wider
            q_len = samples // 4
            r_len = samples // 2
            s_len = samples - q_len - r_len
            q = -0.2 * np.sin(np.linspace(0, np.pi, q_len))
            r = 1.2 * np.sin(np.linspace(0, np.pi, r_len))
            s = -0.4 * np.sin(np.linspace(0, np.pi, s_len))
            wave = np.concatenate([q, r, s])
        elif self.shape == 'flutter':
            # Sawtooth flutter waves
            cycles = int(samples / 30)  # Approx 300/min
            if cycles < 1:
                cycles = 1
            single = np.linspace(0.2, -0.2, samples // cycles)
            wave = np.tile(single, cycles)[:samples]
        elif self.shape == 'fibrillation':
            # Chaotic baseline for AF
            wave = 0.1 * np.random.randn(samples)
            # Add some low-frequency modulation
            wave += 0.05 * np.sin(np.linspace(0, 8*np.pi, samples))
        elif self.shape == 'vf':
            # Ventricular fibrillation - chaotic
            t = np.linspace(0, 4*np.pi, samples)
            wave = np.sin(t + np.random.randn(samples) * 0.5)
            wave += 0.3 * np.random.randn(samples)
        else:
            wave = np.zeros(samples)
        
        # Apply amplitude and polarity
        wave = wave * self.amplitude * self.polarity
        
        # Apply skew if needed
        if self.skew != 0:
            shift = int(len(wave) * self.skew * 0.2)
            wave = np.roll(wave, shift)
            
        return wave


@dataclass  
class ECGTemplate:
    """Complete ECG template for one cardiac cycle."""
    name: str
    arrhythmia_type: ArrhythmiaType
    
    # Wave components
    p_wave: Optional[WaveTemplate] = None
    qrs_complex: WaveTemplate = field(default_factory=lambda: WaveTemplate(1.0, 80, 'qrs'))
    t_wave: Optional[WaveTemplate] = None
    
    # Timing (ms)
    pr_interval: float = 160      # P onset to QRS onset
    qt_interval: float = 400      # QRS onset to T end
    
    # Rhythm
    rate_bpm: Tuple[int, int] = (60, 100)  # (min, max) heart rate
    rr_variability: float = 0.05  # RR interval variation coefficient
    regularity: str = 'regular'   # 'regular', 'irregular', 'chaotic'
    
    # Special patterns
    pattern: Optional[str] = None  # 'bigeminy', 'trigeminy', 'grouped', None
    baseline: str = 'flat'         # 'flat', 'fibrillatory', 'flutter', 'chaotic'
    
    # Lead-specific modifications
    lead_adjustments: Dict[str, float] = field(default_factory=dict)
    
    def generate_beat(self, sampling_rate: int = 500, lead: str = 'II') -> np.ndarray:
        """Generate one complete cardiac cycle."""
        rate = np.mean(self.rate_bpm)
        rr_ms = 60000 / rate  # RR interval in ms
        total_samples = int(rr_ms * sampling_rate / 1000)
        
        beat = np.zeros(total_samples)
        
        # Get lead adjustment
        lead_scale = self.lead_adjustments.get(lead, 1.0)
        
        # Add baseline if needed
        if self.baseline == 'fibrillatory':
            beat += 0.05 * np.random.randn(total_samples)
        elif self.baseline == 'flutter':
            flutter = WaveTemplate(0.2, rr_ms, 'flutter')
            beat += flutter.generate(sampling_rate)[:total_samples]
        elif self.baseline == 'chaotic':
            vf = WaveTemplate(1.0, rr_ms, 'vf')
            return vf.generate(sampling_rate)[:total_samples] * lead_scale
        
        pos = 0
        
        # P wave
        if self.p_wave is not None:
            p = self.p_wave.generate(sampling_rate)
            p_len = min(len(p), total_samples - pos)
            beat[pos:pos + p_len] += p[:p_len]
        
        # PR segment (flat)
        pos = int(self.pr_interval * sampling_rate / 1000)
        
        # QRS complex
        qrs = self.qrs_complex.generate(sampling_rate)
        qrs_len = min(len(qrs), total_samples - pos)
        if qrs_len > 0:
            beat[pos:pos + qrs_len] += qrs[:qrs_len]
        
        # ST segment + T wave
        if self.t_wave is not None:
            t_pos = pos + len(qrs) + int(80 * sampling_rate / 1000)  # ST segment ~80ms
            t = self.t_wave.generate(sampling_rate)
            t_len = min(len(t), total_samples - t_pos)
            if t_len > 0 and t_pos < total_samples:
                beat[t_pos:t_pos + t_len] += t[:t_len]
        
        return beat * lead_scale


# =============================================================================
# TEMPLATE DEFINITIONS - 10 PRIORITY ARRHYTHMIAS
# =============================================================================

TEMPLATES: Dict[ArrhythmiaType, ECGTemplate] = {
    
    # =========================================================================
    # 1. NORMAL SINUS RHYTHM (Baseline)
    # =========================================================================
    ArrhythmiaType.NORMAL_SINUS: ECGTemplate(
        name="Normal Sinus Rhythm",
        arrhythmia_type=ArrhythmiaType.NORMAL_SINUS,
        p_wave=WaveTemplate(amplitude=0.15, duration_ms=80, shape='gaussian'),
        qrs_complex=WaveTemplate(amplitude=1.0, duration_ms=80, shape='qrs'),
        t_wave=WaveTemplate(amplitude=0.3, duration_ms=160, shape='gaussian'),
        pr_interval=160,
        qt_interval=400,
        rate_bpm=(60, 100),
        rr_variability=0.05,
        regularity='regular',
        baseline='flat',
        lead_adjustments={
            'I': 0.8, 'II': 1.0, 'III': 0.6,
            'aVR': -0.5, 'aVL': 0.5, 'aVF': 0.8,
            'V1': -0.4, 'V2': 0.3, 'V3': 0.7,
            'V4': 1.0, 'V5': 0.9, 'V6': 0.8
        }
    ),
    
    # =========================================================================
    # 2. SINUS BRADYCARDIA
    # =========================================================================
    ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA: ECGTemplate(
        name="Sinus Bradycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA,
        p_wave=WaveTemplate(amplitude=0.15, duration_ms=80, shape='gaussian'),
        qrs_complex=WaveTemplate(amplitude=1.0, duration_ms=80, shape='qrs'),
        t_wave=WaveTemplate(amplitude=0.3, duration_ms=160, shape='gaussian'),
        pr_interval=160,
        qt_interval=440,  # Slightly prolonged
        rate_bpm=(35, 59),
        rr_variability=0.03,
        regularity='regular',
        baseline='flat'
    ),
    
    # =========================================================================
    # 3. SINUS TACHYCARDIA
    # =========================================================================
    ArrhythmiaType.SUPRA_TACHY_SINUS_TACHYCARDIA: ECGTemplate(
        name="Sinus Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_SINUS_TACHYCARDIA,
        p_wave=WaveTemplate(amplitude=0.18, duration_ms=70, shape='gaussian'),  # Slightly taller
        qrs_complex=WaveTemplate(amplitude=1.0, duration_ms=80, shape='qrs'),
        t_wave=WaveTemplate(amplitude=0.25, duration_ms=140, shape='gaussian'),  # Shorter cycle
        pr_interval=140,  # Shorter
        qt_interval=320,  # Shorter with rate
        rate_bpm=(100, 180),
        rr_variability=0.08,
        regularity='regular',
        baseline='flat'
    ),
    
    # =========================================================================
    # 4. ATRIAL FIBRILLATION
    # =========================================================================
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION: ECGTemplate(
        name="Atrial Fibrillation",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
        p_wave=None,  # NO P WAVES - KEY FEATURE
        qrs_complex=WaveTemplate(amplitude=1.0, duration_ms=80, shape='qrs'),
        t_wave=WaveTemplate(amplitude=0.3, duration_ms=160, shape='gaussian'),
        pr_interval=0,  # No PR
        qt_interval=380,
        rate_bpm=(60, 160),
        rr_variability=0.30,  # HIGH VARIABILITY - IRREGULARLY IRREGULAR
        regularity='chaotic',
        baseline='fibrillatory'  # Fibrillatory baseline
    ),
    
    # =========================================================================
    # 5. ATRIAL FLUTTER
    # =========================================================================
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER: ECGTemplate(
        name="Atrial Flutter",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER,
        p_wave=None,  # Flutter waves instead
        qrs_complex=WaveTemplate(amplitude=1.0, duration_ms=80, shape='qrs'),
        t_wave=WaveTemplate(amplitude=0.25, duration_ms=140, shape='gaussian'),
        pr_interval=0,
        qt_interval=360,
        rate_bpm=(130, 150),  # Typically 2:1 block of 300 atrial rate
        rr_variability=0.02,  # Usually regular
        regularity='regular',
        baseline='flutter'  # SAWTOOTH FLUTTER WAVES
    ),
    
    # =========================================================================
    # 6. VENTRICULAR TACHYCARDIA (Monomorphic)
    # =========================================================================
    ArrhythmiaType.VENT_VT_MONO: ECGTemplate(
        name="Monomorphic Ventricular Tachycardia",
        arrhythmia_type=ArrhythmiaType.VENT_VT_MONO,
        p_wave=None,  # AV dissociation - P may be seen independently
        qrs_complex=WaveTemplate(amplitude=1.5, duration_ms=140, shape='wide_qrs'),  # WIDE QRS
        t_wave=WaveTemplate(amplitude=-0.4, duration_ms=120, shape='gaussian', polarity=-1),  # Opposite polarity
        pr_interval=0,
        qt_interval=300,
        rate_bpm=(140, 220),
        rr_variability=0.02,
        regularity='regular',  # Monomorphic = regular
        baseline='flat'
    ),
    
    # =========================================================================
    # 7. VENTRICULAR FIBRILLATION (Coarse)
    # =========================================================================
    ArrhythmiaType.VENT_VF_COARSE: ECGTemplate(
        name="Ventricular Fibrillation (Coarse)",
        arrhythmia_type=ArrhythmiaType.VENT_VF_COARSE,
        p_wave=None,
        qrs_complex=WaveTemplate(amplitude=0.8, duration_ms=200, shape='vf'),  # Chaotic
        t_wave=None,
        pr_interval=0,
        qt_interval=0,
        rate_bpm=(300, 500),  # Chaos
        rr_variability=0.5,
        regularity='chaotic',
        baseline='chaotic'  # COMPLETELY CHAOTIC
    ),
    
    # =========================================================================
    # 8. PVC (Premature Ventricular Contraction)
    # =========================================================================
    ArrhythmiaType.VENT_PVC: ECGTemplate(
        name="Premature Ventricular Contraction",
        arrhythmia_type=ArrhythmiaType.VENT_PVC,
        p_wave=None,  # No P for the PVC beat
        qrs_complex=WaveTemplate(amplitude=1.8, duration_ms=140, shape='wide_qrs'),  # Wide bizarre
        t_wave=WaveTemplate(amplitude=-0.5, duration_ms=140, shape='gaussian', polarity=-1),
        pr_interval=0,
        qt_interval=350,
        rate_bpm=(60, 100),  # Base rhythm
        rr_variability=0.05,
        regularity='regular',
        pattern='bigeminy',  # Can be bigeminy, trigeminy, etc.
        baseline='flat'
    ),
    
    # =========================================================================
    # 9. COMPLETE AV BLOCK (3rd Degree)
    # =========================================================================
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3: ECGTemplate(
        name="Complete AV Block",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3,
        p_wave=WaveTemplate(amplitude=0.15, duration_ms=80, shape='gaussian'),  # P waves present
        qrs_complex=WaveTemplate(amplitude=1.2, duration_ms=120, shape='wide_qrs'),  # Escape rhythm
        t_wave=WaveTemplate(amplitude=0.35, duration_ms=160, shape='gaussian'),
        pr_interval=0,  # NO RELATIONSHIP between P and QRS
        qt_interval=450,
        rate_bpm=(30, 45),  # Slow escape rhythm
        rr_variability=0.02,
        regularity='regular',  # QRS regular, P regular, but INDEPENDENT
        baseline='flat'
    ),
    
    # =========================================================================
    # 10. ASYSTOLE
    # =========================================================================
    ArrhythmiaType.VENT_ASYSTOLE: ECGTemplate(
        name="Asystole",
        arrhythmia_type=ArrhythmiaType.VENT_ASYSTOLE,
        p_wave=None,  # Maybe occasional P
        qrs_complex=WaveTemplate(amplitude=0.0, duration_ms=0, shape='gaussian'),  # NO QRS
        t_wave=None,
        pr_interval=0,
        qt_interval=0,
        rate_bpm=(0, 0),  # NO RATE
        rr_variability=0,
        regularity='regular',  # Flatline is "regular"
        baseline='flat'  # FLATLINE
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_template(arrhythmia: ArrhythmiaType) -> ECGTemplate:
    """
    Get ECG template for an arrhythmia.
    
    Args:
        arrhythmia: ArrhythmiaType enum value
        
    Returns:
        ECGTemplate object
        
    Raises:
        ValueError: If template not found
    """
    if arrhythmia in TEMPLATES:
        return TEMPLATES[arrhythmia]
    
    # Return normal sinus as fallback for unimplemented arrhythmias
    print(f"Warning: Template for {arrhythmia.value} not implemented, using Normal Sinus")
    return TEMPLATES[ArrhythmiaType.NORMAL_SINUS]


def list_implemented_templates() -> List[str]:
    """Get list of implemented arrhythmia templates."""
    return [t.name for t in TEMPLATES.values()]


def get_template_stats() -> dict:
    """Get statistics about implemented templates."""
    return {
        'implemented': len(TEMPLATES),
        'total': len(ArrhythmiaType),
        'coverage': f"{len(TEMPLATES) / len(ArrhythmiaType) * 100:.1f}%",
        'arrhythmias': list_implemented_templates()
    }
