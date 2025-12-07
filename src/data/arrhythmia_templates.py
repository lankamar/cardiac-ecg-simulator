"""
ECG Arrhythmia Templates - COMPLETE 54 ARRHYTHMIAS.

Contains normalized ECG templates for ALL 54 cardiac arrhythmias.
Each template defines the exact morphology for P, QRS, T waves and
their timing relationships for fast lookup-based generation.

Categories:
- Supraventricular Bradyarrhythmias: 6
- Supraventricular Tachyarrhythmias: 14  
- Other Supraventricular: 10
- Ventricular: 16
- Special Phenomena: 8
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np

from src.arrhythmias.types import ArrhythmiaType


# =============================================================================
# TEMPLATE DATA STRUCTURES
# =============================================================================

@dataclass
class WaveTemplate:
    """Template for a single ECG wave component."""
    amplitude: float        # Peak amplitude in mV
    duration_ms: float      # Duration in milliseconds
    shape: str              # 'gaussian', 'triangle', 'sawtooth', 'qrs', 'wide_qrs', etc.
    polarity: int = 1       # 1 = positive, -1 = negative
    skew: float = 0.0       # Asymmetry factor
    
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
            wave = np.concatenate([np.linspace(0, 1, half), np.linspace(1, 0, samples - half)])
        elif self.shape == 'sawtooth':
            wave = np.linspace(1, -1, samples)
        elif self.shape == 'sine':
            wave = np.sin(np.linspace(0, np.pi, samples))
        elif self.shape == 'noise':
            wave = np.random.randn(samples) * 0.5
        elif self.shape == 'qrs':
            q_len, r_len = samples // 5, samples // 3
            s_len = samples - q_len - r_len
            q = -0.15 * np.sin(np.linspace(0, np.pi, q_len))
            r = np.sin(np.linspace(0, np.pi, r_len))
            s = -0.3 * np.sin(np.linspace(0, np.pi, s_len))
            wave = np.concatenate([q, r, s])
        elif self.shape == 'wide_qrs':
            samples = int(samples * 1.5)
            q_len, r_len = samples // 4, samples // 2
            s_len = samples - q_len - r_len
            q = -0.2 * np.sin(np.linspace(0, np.pi, q_len))
            r = 1.2 * np.sin(np.linspace(0, np.pi, r_len))
            s = -0.4 * np.sin(np.linspace(0, np.pi, s_len))
            wave = np.concatenate([q, r, s])
        elif self.shape == 'delta':
            # Delta wave for WPW - slurred upstroke
            delta_len = samples // 3
            qrs_len = samples - delta_len
            delta = np.linspace(0, 0.3, delta_len)
            qrs = 0.3 + 0.7 * np.sin(np.linspace(0, np.pi, qrs_len))
            wave = np.concatenate([delta, qrs])
        elif self.shape == 'flutter':
            cycles = max(1, int(samples / 30))
            single = np.linspace(0.2, -0.2, samples // cycles)
            wave = np.tile(single, cycles)[:samples]
        elif self.shape == 'fibrillation':
            wave = 0.1 * np.random.randn(samples)
            wave += 0.05 * np.sin(np.linspace(0, 8*np.pi, samples))
        elif self.shape == 'vf_coarse':
            t = np.linspace(0, 4*np.pi, samples)
            wave = np.sin(t + np.random.randn(samples) * 0.5)
            wave += 0.3 * np.random.randn(samples)
        elif self.shape == 'vf_fine':
            t = np.linspace(0, 6*np.pi, samples)
            wave = 0.3 * np.sin(t + np.random.randn(samples) * 0.3)
            wave += 0.1 * np.random.randn(samples)
        elif self.shape == 'torsades':
            # Twisting axis
            t = np.linspace(0, 4*np.pi, samples)
            modulation = np.sin(np.linspace(0, 2*np.pi, samples))
            wave = np.sin(t) * (0.5 + 0.5 * modulation)
        elif self.shape == 'brugada':
            # Coved ST elevation
            st = 0.3 * np.exp(-np.linspace(0, 2, samples // 2)**2)
            t_inv = -0.2 * np.sin(np.linspace(0, np.pi, samples - samples // 2))
            wave = np.concatenate([st, t_inv])
        else:
            wave = np.zeros(samples)
        
        wave = wave * self.amplitude * self.polarity
        if self.skew != 0:
            shift = int(len(wave) * self.skew * 0.2)
            wave = np.roll(wave, shift)
        return wave


@dataclass  
class ECGTemplate:
    """Complete ECG template for one cardiac cycle."""
    name: str
    arrhythmia_type: ArrhythmiaType
    
    p_wave: Optional[WaveTemplate] = None
    qrs_complex: WaveTemplate = field(default_factory=lambda: WaveTemplate(1.0, 80, 'qrs'))
    t_wave: Optional[WaveTemplate] = None
    
    pr_interval: float = 160
    qt_interval: float = 400
    rate_bpm: Tuple[int, int] = (60, 100)
    rr_variability: float = 0.05
    regularity: str = 'regular'
    pattern: Optional[str] = None
    baseline: str = 'flat'
    lead_adjustments: Dict[str, float] = field(default_factory=dict)
    
    def generate_beat(self, sampling_rate: int = 500, lead: str = 'II') -> np.ndarray:
        """Generate one complete cardiac cycle."""
        rate = np.mean(self.rate_bpm)
        if rate <= 0:
            rate = 60
        rr_ms = 60000 / rate
        total_samples = int(rr_ms * sampling_rate / 1000)
        beat = np.zeros(total_samples)
        lead_scale = self.lead_adjustments.get(lead, 1.0)
        
        # Add baseline patterns
        if self.baseline == 'fibrillatory':
            beat += 0.05 * np.random.randn(total_samples)
        elif self.baseline == 'flutter':
            flutter = WaveTemplate(0.2, rr_ms, 'flutter')
            f = flutter.generate(sampling_rate)
            beat[:min(len(f), total_samples)] += f[:min(len(f), total_samples)]
        elif self.baseline == 'chaotic':
            vf = WaveTemplate(1.0, rr_ms, 'vf_coarse')
            return vf.generate(sampling_rate)[:total_samples] * lead_scale
        elif self.baseline == 'chaotic_fine':
            vf = WaveTemplate(0.3, rr_ms, 'vf_fine')
            return vf.generate(sampling_rate)[:total_samples] * lead_scale
        elif self.baseline == 'torsades':
            tors = WaveTemplate(1.0, rr_ms, 'torsades')
            return tors.generate(sampling_rate)[:total_samples] * lead_scale
        
        pos = 0
        
        # P wave
        if self.p_wave is not None:
            p = self.p_wave.generate(sampling_rate)
            p_len = min(len(p), total_samples - pos)
            beat[pos:pos + p_len] += p[:p_len]
        
        # QRS position
        pos = int(self.pr_interval * sampling_rate / 1000)
        if pos >= total_samples:
            pos = total_samples // 4
        
        # QRS complex
        qrs = self.qrs_complex.generate(sampling_rate)
        qrs_len = min(len(qrs), total_samples - pos)
        if qrs_len > 0:
            beat[pos:pos + qrs_len] += qrs[:qrs_len]
        
        # T wave
        if self.t_wave is not None:
            t_pos = pos + len(qrs) + int(80 * sampling_rate / 1000)
            t = self.t_wave.generate(sampling_rate)
            t_len = min(len(t), total_samples - t_pos)
            if t_len > 0 and t_pos < total_samples:
                beat[t_pos:t_pos + t_len] += t[:t_len]
        
        return beat * lead_scale


# =============================================================================
# COMPLETE 54 ARRHYTHMIA TEMPLATES
# =============================================================================

TEMPLATES: Dict[ArrhythmiaType, ECGTemplate] = {
    
    # =========================================================================
    # NORMAL (1)
    # =========================================================================
    ArrhythmiaType.NORMAL_SINUS: ECGTemplate(
        name="Normal Sinus Rhythm",
        arrhythmia_type=ArrhythmiaType.NORMAL_SINUS,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), regularity='regular',
        lead_adjustments={'I': 0.8, 'II': 1.0, 'III': 0.6, 'aVR': -0.5, 'aVL': 0.5, 'aVF': 0.8,
                          'V1': -0.4, 'V2': 0.3, 'V3': 0.7, 'V4': 1.0, 'V5': 0.9, 'V6': 0.8}
    ),
    
    # =========================================================================
    # SUPRAVENTRICULAR BRADYARRHYTHMIAS (6)
    # =========================================================================
    ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA: ECGTemplate(
        name="Sinus Bradycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(35, 59), qt_interval=440, regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_BRADY_SICK_SINUS: ECGTemplate(
        name="Sick Sinus Syndrome",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_SICK_SINUS,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(30, 100), rr_variability=0.35, regularity='irregular', pattern='pauses'
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_1: ECGTemplate(
        name="First Degree AV Block",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_1,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        pr_interval=280,  # Prolonged > 200ms (KEY FEATURE)
        rate_bpm=(50, 90), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH: ECGTemplate(
        name="Second Degree AV Block Type I (Wenckebach)",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        pr_interval=200, rate_bpm=(40, 80),
        regularity='irregular', pattern='wenckebach'  # Progressive PR then drop
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_MOBITZ: ECGTemplate(
        name="Second Degree AV Block Type II (Mobitz II)",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_MOBITZ,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 120, 'wide_qrs'),  # Often wide QRS
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        pr_interval=180, rate_bpm=(30, 70),
        regularity='irregular', pattern='mobitz'  # Fixed PR then sudden drop
    ),
    
    ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3: ECGTemplate(
        name="Complete (Third Degree) AV Block",
        arrhythmia_type=ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),  # P waves present but independent
        qrs_complex=WaveTemplate(1.2, 120, 'wide_qrs'),  # Escape rhythm
        t_wave=WaveTemplate(0.35, 160, 'gaussian'),
        pr_interval=0,  # NO RELATIONSHIP (KEY FEATURE)
        rate_bpm=(30, 45), regularity='regular', pattern='av_dissociation'
    ),
    
    # =========================================================================
    # SUPRAVENTRICULAR TACHYARRHYTHMIAS (14)
    # =========================================================================
    ArrhythmiaType.SUPRA_TACHY_SINUS_TACHYCARDIA: ECGTemplate(
        name="Sinus Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_SINUS_TACHYCARDIA,
        p_wave=WaveTemplate(0.18, 70, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        pr_interval=140, qt_interval=320,
        rate_bpm=(100, 180), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_TACHYCARDIA: ECGTemplate(
        name="Atrial Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_TACHYCARDIA,
        p_wave=WaveTemplate(0.12, 70, 'gaussian'),  # Different P morphology
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        pr_interval=140, rate_bpm=(150, 250), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER: ECGTemplate(
        name="Atrial Flutter",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER,
        p_wave=None,  # Flutter waves instead (SAWTOOTH)
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        pr_interval=0, rate_bpm=(130, 150),
        regularity='regular', baseline='flutter'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION: ECGTemplate(
        name="Atrial Fibrillation",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
        p_wave=None,  # NO P WAVES (KEY FEATURE)
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        pr_interval=0, rate_bpm=(60, 160),
        rr_variability=0.30, regularity='chaotic',  # IRREGULARLY IRREGULAR
        baseline='fibrillatory'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_AVNRT: ECGTemplate(
        name="AV Nodal Reentrant Tachycardia (AVNRT)",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_AVNRT,
        p_wave=None,  # P hidden in QRS (pseudo-R' in V1)
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        pr_interval=80, rate_bpm=(140, 220), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_AVRT: ECGTemplate(
        name="AV Reentrant Tachycardia (AVRT)",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_AVRT,
        p_wave=WaveTemplate(0.1, 60, 'gaussian', polarity=-1),  # Retrograde P
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        pr_interval=100, rate_bpm=(140, 250), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_WPW: ECGTemplate(
        name="Wolff-Parkinson-White Syndrome",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_WPW,
        p_wave=WaveTemplate(0.15, 70, 'gaussian'),
        qrs_complex=WaveTemplate(1.2, 130, 'delta'),  # DELTA WAVE (KEY FEATURE)
        t_wave=WaveTemplate(0.3, 140, 'gaussian'),
        pr_interval=100,  # SHORT PR < 120ms
        rate_bpm=(100, 250), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_PSVT: ECGTemplate(
        name="Paroxysmal Supraventricular Tachycardia (PSVT)",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_PSVT,
        p_wave=None,  # Often not visible
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        pr_interval=0, rate_bpm=(150, 220), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_MAT: ECGTemplate(
        name="Multifocal Atrial Tachycardia (MAT)",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_MAT,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),  # ≥3 different P morphologies
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(100, 180), rr_variability=0.20,
        regularity='irregular', pattern='mat'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_FOCAL_AT: ECGTemplate(
        name="Focal Atrial Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_FOCAL_AT,
        p_wave=WaveTemplate(0.12, 70, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        rate_bpm=(150, 250), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_INTRA_ATRIAL_REENTRY: ECGTemplate(
        name="Intra-atrial Reentrant Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_INTRA_ATRIAL_REENTRY,
        p_wave=WaveTemplate(0.12, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        rate_bpm=(130, 200), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_SINUS_NODE_REENTRY: ECGTemplate(
        name="Sinus Node Reentrant Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_SINUS_NODE_REENTRY,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),  # P identical to sinus
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(100, 150), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_ECTOPIC_ATRIAL: ECGTemplate(
        name="Ectopic Atrial Rhythm",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ECTOPIC_ATRIAL,
        p_wave=WaveTemplate(0.12, 80, 'gaussian'),  # Different P
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER_ATYPICAL: ECGTemplate(
        name="Atypical Atrial Flutter",
        arrhythmia_type=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER_ATYPICAL,
        p_wave=None,
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        rate_bpm=(120, 200), baseline='flutter', regularity='regular'
    ),
    
    # =========================================================================
    # OTHER SUPRAVENTRICULAR (10)
    # =========================================================================
    ArrhythmiaType.SUPRA_OTHER_PAC: ECGTemplate(
        name="Premature Atrial Contraction (PAC)",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_PAC,
        p_wave=WaveTemplate(0.12, 70, 'gaussian'),  # Early, different P
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), pattern='premature'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_PJC: ECGTemplate(
        name="Premature Junctional Contraction (PJC)",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_PJC,
        p_wave=None,  # No P or retrograde
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), pattern='premature'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_JUNCTIONAL_ESCAPE: ECGTemplate(
        name="Junctional Escape Rhythm",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_JUNCTIONAL_ESCAPE,
        p_wave=None,  # No P or retrograde
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(40, 60), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_JUNCTIONAL_TACHY: ECGTemplate(
        name="Junctional Tachycardia",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_JUNCTIONAL_TACHY,
        p_wave=None,
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(70, 130), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_JET: ECGTemplate(
        name="Junctional Ectopic Tachycardia (JET)",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_JET,
        p_wave=None,  # AV dissociation
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.25, 140, 'gaussian'),
        rate_bpm=(120, 200), regularity='regular'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_WANDERING_PACEMAKER: ECGTemplate(
        name="Wandering Atrial Pacemaker",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_WANDERING_PACEMAKER,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),  # ≥3 P morphologies
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), rr_variability=0.15,
        regularity='irregular', pattern='wandering'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_SINUS_ARRHYTHMIA: ECGTemplate(
        name="Sinus Arrhythmia",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_SINUS_ARRHYTHMIA,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), rr_variability=0.15,
        regularity='irregular'  # Varies with respiration
    ),
    
    ArrhythmiaType.SUPRA_OTHER_SINUS_PAUSE: ECGTemplate(
        name="Sinus Pause",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_SINUS_PAUSE,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(50, 80), pattern='pause'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_SINUS_ARREST: ECGTemplate(
        name="Sinus Arrest",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_SINUS_ARREST,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 100, 'qrs'),  # Escape
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(30, 60), pattern='arrest'
    ),
    
    ArrhythmiaType.SUPRA_OTHER_SINOATRIAL_BLOCK: ECGTemplate(
        name="Sinoatrial Exit Block",
        arrhythmia_type=ArrhythmiaType.SUPRA_OTHER_SINOATRIAL_BLOCK,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(50, 80), pattern='sa_block'
    ),
    
    # =========================================================================
    # VENTRICULAR ARRHYTHMIAS (16)
    # =========================================================================
    ArrhythmiaType.VENT_PVC: ECGTemplate(
        name="Premature Ventricular Contraction (PVC)",
        arrhythmia_type=ArrhythmiaType.VENT_PVC,
        p_wave=None,  # No preceding P
        qrs_complex=WaveTemplate(1.8, 140, 'wide_qrs'),  # WIDE, BIZARRE
        t_wave=WaveTemplate(0.5, 140, 'gaussian', polarity=-1),  # Opposite T
        rate_bpm=(60, 100), pattern='pvc'
    ),
    
    ArrhythmiaType.VENT_PVC_BIGEMINY: ECGTemplate(
        name="PVC Bigeminy",
        arrhythmia_type=ArrhythmiaType.VENT_PVC_BIGEMINY,
        p_wave=None,
        qrs_complex=WaveTemplate(1.8, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.5, 140, 'gaussian', polarity=-1),
        rate_bpm=(60, 100), pattern='bigeminy'  # Normal-PVC-Normal-PVC
    ),
    
    ArrhythmiaType.VENT_PVC_TRIGEMINY: ECGTemplate(
        name="PVC Trigeminy",
        arrhythmia_type=ArrhythmiaType.VENT_PVC_TRIGEMINY,
        p_wave=None,
        qrs_complex=WaveTemplate(1.8, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.5, 140, 'gaussian', polarity=-1),
        rate_bpm=(60, 100), pattern='trigeminy'  # Normal-Normal-PVC
    ),
    
    ArrhythmiaType.VENT_PVC_COUPLET: ECGTemplate(
        name="PVC Couplet",
        arrhythmia_type=ArrhythmiaType.VENT_PVC_COUPLET,
        p_wave=None,
        qrs_complex=WaveTemplate(1.8, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.5, 140, 'gaussian', polarity=-1),
        rate_bpm=(60, 100), pattern='couplet'  # 2 consecutive PVCs
    ),
    
    ArrhythmiaType.VENT_PVC_TRIPLET: ECGTemplate(
        name="PVC Triplet (NSVT)",
        arrhythmia_type=ArrhythmiaType.VENT_PVC_TRIPLET,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.4, 120, 'gaussian', polarity=-1),
        rate_bpm=(140, 200), pattern='triplet'  # 3 PVCs = brief NSVT
    ),
    
    ArrhythmiaType.VENT_AIVR: ECGTemplate(
        name="Accelerated Idioventricular Rhythm (AIVR)",
        arrhythmia_type=ArrhythmiaType.VENT_AIVR,
        p_wave=None,
        qrs_complex=WaveTemplate(1.3, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.4, 140, 'gaussian', polarity=-1),
        rate_bpm=(40, 110), regularity='regular'  # Slow VT
    ),
    
    ArrhythmiaType.VENT_ESCAPE: ECGTemplate(
        name="Ventricular Escape Rhythm",
        arrhythmia_type=ArrhythmiaType.VENT_ESCAPE,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 160, 'wide_qrs'),  # Very wide
        t_wave=WaveTemplate(0.5, 160, 'gaussian', polarity=-1),
        rate_bpm=(20, 40), regularity='regular'
    ),
    
    ArrhythmiaType.VENT_VT_MONO: ECGTemplate(
        name="Monomorphic Ventricular Tachycardia",
        arrhythmia_type=ArrhythmiaType.VENT_VT_MONO,
        p_wave=None,  # AV dissociation
        qrs_complex=WaveTemplate(1.5, 140, 'wide_qrs'),  # UNIFORM WIDE QRS
        t_wave=WaveTemplate(0.4, 120, 'gaussian', polarity=-1),
        rate_bpm=(140, 220), regularity='regular'
    ),
    
    ArrhythmiaType.VENT_VT_POLY: ECGTemplate(
        name="Polymorphic Ventricular Tachycardia",
        arrhythmia_type=ArrhythmiaType.VENT_VT_POLY,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 140, 'wide_qrs'),  # Varying morphology
        t_wave=None,
        rate_bpm=(100, 250), rr_variability=0.2,
        regularity='irregular'
    ),
    
    ArrhythmiaType.VENT_VT_SUSTAINED: ECGTemplate(
        name="Sustained Ventricular Tachycardia",
        arrhythmia_type=ArrhythmiaType.VENT_VT_SUSTAINED,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.4, 120, 'gaussian', polarity=-1),
        rate_bpm=(100, 250), regularity='regular'  # >30s duration
    ),
    
    ArrhythmiaType.VENT_VT_NONSUSTAINED: ECGTemplate(
        name="Non-Sustained Ventricular Tachycardia (NSVT)",
        arrhythmia_type=ArrhythmiaType.VENT_VT_NONSUSTAINED,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.4, 120, 'gaussian', polarity=-1),
        rate_bpm=(100, 250), pattern='nsvt'  # <30s, ≥3 beats
    ),
    
    ArrhythmiaType.VENT_TORSADES: ECGTemplate(
        name="Torsades de Pointes",
        arrhythmia_type=ArrhythmiaType.VENT_TORSADES,
        p_wave=None,
        qrs_complex=WaveTemplate(1.2, 150, 'wide_qrs'),
        t_wave=None,
        rate_bpm=(200, 300),
        baseline='torsades', regularity='irregular'  # TWISTING QRS AXIS
    ),
    
    ArrhythmiaType.VENT_VF_COARSE: ECGTemplate(
        name="Ventricular Fibrillation (Coarse)",
        arrhythmia_type=ArrhythmiaType.VENT_VF_COARSE,
        p_wave=None, t_wave=None,
        qrs_complex=WaveTemplate(0.8, 200, 'vf_coarse'),
        rate_bpm=(300, 500),
        baseline='chaotic', regularity='chaotic'  # AMPLITUDE > 3mm
    ),
    
    ArrhythmiaType.VENT_VF_FINE: ECGTemplate(
        name="Ventricular Fibrillation (Fine)",
        arrhythmia_type=ArrhythmiaType.VENT_VF_FINE,
        p_wave=None, t_wave=None,
        qrs_complex=WaveTemplate(0.3, 200, 'vf_fine'),  # Low amplitude
        rate_bpm=(300, 500),
        baseline='chaotic_fine', regularity='chaotic'  # AMPLITUDE < 3mm
    ),
    
    ArrhythmiaType.VENT_ASYSTOLE: ECGTemplate(
        name="Asystole",
        arrhythmia_type=ArrhythmiaType.VENT_ASYSTOLE,
        p_wave=None, t_wave=None,
        qrs_complex=WaveTemplate(0.0, 0, 'gaussian'),  # FLATLINE
        rate_bpm=(0, 0), regularity='regular'
    ),
    
    ArrhythmiaType.VENT_IDIOVENTRICULAR: ECGTemplate(
        name="Idioventricular Rhythm",
        arrhythmia_type=ArrhythmiaType.VENT_IDIOVENTRICULAR,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 160, 'wide_qrs'),
        t_wave=WaveTemplate(0.5, 160, 'gaussian', polarity=-1),
        rate_bpm=(20, 40), regularity='regular'  # Very slow escape
    ),
    
    # =========================================================================
    # SPECIAL PHENOMENA (8)
    # =========================================================================
    ArrhythmiaType.SPECIAL_PARASYSTOLE: ECGTemplate(
        name="Parasystole",
        arrhythmia_type=ArrhythmiaType.SPECIAL_PARASYSTOLE,
        p_wave=None,
        qrs_complex=WaveTemplate(1.5, 140, 'wide_qrs'),
        t_wave=WaveTemplate(0.4, 140, 'gaussian', polarity=-1),
        rate_bpm=(60, 100), pattern='parasystole'  # Fixed interectopic intervals
    ),
    
    ArrhythmiaType.SPECIAL_FUSION_BEAT: ECGTemplate(
        name="Fusion Beat",
        arrhythmia_type=ArrhythmiaType.SPECIAL_FUSION_BEAT,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.2, 100, 'qrs'),  # Intermediate morphology
        t_wave=WaveTemplate(0.3, 150, 'gaussian'),
        rate_bpm=(60, 100), pattern='fusion'
    ),
    
    ArrhythmiaType.SPECIAL_CAPTURE_BEAT: ECGTemplate(
        name="Capture Beat",
        arrhythmia_type=ArrhythmiaType.SPECIAL_CAPTURE_BEAT,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),  # Normal QRS in VT
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(140, 200), pattern='capture'
    ),
    
    ArrhythmiaType.SPECIAL_R_ON_T: ECGTemplate(
        name="R-on-T Phenomenon",
        arrhythmia_type=ArrhythmiaType.SPECIAL_R_ON_T,
        p_wave=None,
        qrs_complex=WaveTemplate(1.8, 140, 'wide_qrs'),  # PVC on T wave
        t_wave=WaveTemplate(0.5, 140, 'gaussian', polarity=-1),
        rate_bpm=(60, 100), pattern='r_on_t'  # Dangerous - can trigger VF
    ),
    
    ArrhythmiaType.SPECIAL_ASHMAN: ECGTemplate(
        name="Ashman Phenomenon",
        arrhythmia_type=ArrhythmiaType.SPECIAL_ASHMAN,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.2, 120, 'wide_qrs'),  # Aberrant after long-short
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(80, 140), pattern='ashman'
    ),
    
    ArrhythmiaType.SPECIAL_CONCEALED_CONDUCTION: ECGTemplate(
        name="Concealed Conduction",
        arrhythmia_type=ArrhythmiaType.SPECIAL_CONCEALED_CONDUCTION,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 80, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        rate_bpm=(60, 100), pattern='concealed'
    ),
    
    ArrhythmiaType.SPECIAL_AV_DISSOCIATION: ECGTemplate(
        name="AV Dissociation",
        arrhythmia_type=ArrhythmiaType.SPECIAL_AV_DISSOCIATION,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),  # Independent P
        qrs_complex=WaveTemplate(1.2, 100, 'qrs'),
        t_wave=WaveTemplate(0.3, 160, 'gaussian'),
        pr_interval=0,  # No relationship
        rate_bpm=(60, 100), pattern='dissociation'
    ),
    
    ArrhythmiaType.SPECIAL_BRUGADA_PATTERN: ECGTemplate(
        name="Brugada Pattern",
        arrhythmia_type=ArrhythmiaType.SPECIAL_BRUGADA_PATTERN,
        p_wave=WaveTemplate(0.15, 80, 'gaussian'),
        qrs_complex=WaveTemplate(1.0, 100, 'brugada'),  # Coved ST in V1-V3
        t_wave=WaveTemplate(0.2, 160, 'gaussian', polarity=-1),
        rate_bpm=(60, 100), regularity='regular'
    ),
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_template(arrhythmia: ArrhythmiaType) -> ECGTemplate:
    """Get ECG template for an arrhythmia."""
    if arrhythmia in TEMPLATES:
        return TEMPLATES[arrhythmia]
    raise ValueError(f"Template for {arrhythmia.value} not found")


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


def get_templates_by_category() -> Dict[str, List[ECGTemplate]]:
    """Get templates organized by category."""
    categories = {
        'supraventricular_brady': [],
        'supraventricular_tachy': [],
        'supraventricular_other': [],
        'ventricular': [],
        'special': [],
        'normal': []
    }
    
    for arr_type, template in TEMPLATES.items():
        if arr_type == ArrhythmiaType.NORMAL_SINUS:
            categories['normal'].append(template)
        elif 'SUPRA_BRADY' in arr_type.name:
            categories['supraventricular_brady'].append(template)
        elif 'SUPRA_TACHY' in arr_type.name:
            categories['supraventricular_tachy'].append(template)
        elif 'SUPRA_OTHER' in arr_type.name:
            categories['supraventricular_other'].append(template)
        elif 'VENT' in arr_type.name:
            categories['ventricular'].append(template)
        elif 'SPECIAL' in arr_type.name:
            categories['special'].append(template)
    
    return categories
