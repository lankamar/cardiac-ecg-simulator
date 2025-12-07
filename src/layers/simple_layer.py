"""
Simple Layer - Fast ECG Generation.

Uses lookup tables and direct morphology patterns for <1ms latency.
Ideal for real-time training applications.
"""

from typing import Dict, List
import numpy as np
from src.layers.base import BaseLayer


class SimpleLayer(BaseLayer):
    """
    Simple simulation layer using lookup tables.
    
    Characteristics:
    - Latency: <1ms
    - Accuracy: Low-Medium
    - Use case: Training, real-time display
    
    Implementation:
    - Pre-computed waveform templates
    - Direct morphology generation
    - Fast RR interval calculation
    """
    
    def __init__(self, sampling_rate: int = 500):
        super().__init__(sampling_rate)
        self._templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, np.ndarray]:
        """Load pre-computed waveform templates."""
        # P wave template (80ms)
        p_samples = int(0.08 * self.sampling_rate)
        p_wave = self._gaussian_wave(p_samples, amplitude=0.15)
        
        # QRS complex template (80ms)
        qrs_samples = int(0.08 * self.sampling_rate)
        qrs = self._qrs_template(qrs_samples)
        
        # T wave template (160ms)
        t_samples = int(0.16 * self.sampling_rate)
        t_wave = self._gaussian_wave(t_samples, amplitude=0.3)
        
        # Wide QRS for ventricular arrhythmias (140ms)
        wide_qrs_samples = int(0.14 * self.sampling_rate)
        wide_qrs = self._qrs_template(wide_qrs_samples, width_factor=1.75)
        
        return {
            'p_normal': p_wave,
            'qrs_normal': qrs,
            't_normal': t_wave,
            'qrs_wide': wide_qrs,
            'p_inverted': -p_wave,
            'flutter_wave': self._flutter_wave_template(),
        }
    
    def _gaussian_wave(self, samples: int, amplitude: float = 1.0) -> np.ndarray:
        """Generate gaussian-shaped wave."""
        x = np.linspace(-3, 3, samples)
        return amplitude * np.exp(-x**2)
    
    def _qrs_template(self, samples: int, width_factor: float = 1.0) -> np.ndarray:
        """Generate QRS complex template."""
        # Simple QRS: Q dip, R peak, S dip
        qrs = np.zeros(samples)
        third = samples // 3
        
        # Q wave (small negative)
        q_x = np.linspace(0, np.pi, third)
        qrs[:third] = -0.15 * np.sin(q_x)
        
        # R wave (tall positive)
        r_x = np.linspace(0, np.pi, third)
        qrs[third:2*third] = 1.0 * np.sin(r_x)
        
        # S wave (medium negative)
        s_x = np.linspace(0, np.pi, samples - 2*third)
        qrs[2*third:] = -0.3 * np.sin(s_x)
        
        return qrs
    
    def _flutter_wave_template(self) -> np.ndarray:
        """Generate sawtooth flutter wave."""
        samples = int(0.2 * self.sampling_rate)  # 200ms = 300bpm flutter
        x = np.linspace(0, 1, samples)
        return 0.2 * (x - 0.5)  # Sawtooth
    
    def generate(
        self,
        config: 'ArrhythmiaConfig',
        num_samples: int,
        leads: List[str],
        noise_level: float = 0.01,
        hrv: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """
        Generate ECG using lookup tables.
        
        Fast implementation suitable for real-time display.
        """
        signals = {}
        
        # Calculate heart rate and intervals
        rate = np.random.uniform(*config.rate_range)
        rr_interval = 60.0 / rate  # seconds
        rr_samples = int(rr_interval * self.sampling_rate)
        
        for lead in leads:
            signal = np.zeros(num_samples)
            current_pos = 0
            
            while current_pos < num_samples:
                # Apply HRV
                if hrv > 0:
                    rr_var = int(rr_samples * np.random.uniform(-hrv, hrv))
                else:
                    rr_var = 0
                current_rr = rr_samples + rr_var
                
                if current_pos + current_rr > num_samples:
                    break
                
                # Generate one beat based on arrhythmia
                beat = self._generate_beat(config, lead)
                
                # Place beat in signal
                beat_len = min(len(beat), num_samples - current_pos)
                signal[current_pos:current_pos + beat_len] = beat[:beat_len]
                
                current_pos += current_rr
            
            # Add noise
            signal = self._add_noise(signal, noise_level)
            signals[lead] = signal
        
        return signals
    
    def _generate_beat(self, config: 'ArrhythmiaConfig', lead: str) -> np.ndarray:
        """Generate a single heartbeat based on arrhythmia config."""
        rate = np.mean(config.rate_range)
        rr_interval = 60.0 / rate
        beat_samples = int(rr_interval * self.sampling_rate)
        beat = np.zeros(beat_samples)
        
        # Determine which templates to use
        is_ventricular = config.category == 'ventricular'
        has_p_wave = config.p_wave.morphology != 'absent' if hasattr(config, 'p_wave') else True
        
        pos = 0
        
        # P wave (if present)
        if has_p_wave and not is_ventricular:
            p = self._templates['p_normal']
            p_len = len(p)
            if pos + p_len < beat_samples:
                beat[pos:pos + p_len] = p
            pos += p_len + int(0.04 * self.sampling_rate)  # PR segment
        
        # QRS complex
        if is_ventricular:
            qrs = self._templates['qrs_wide']
        else:
            qrs = self._templates['qrs_normal']
        
        qrs_len = len(qrs)
        if pos + qrs_len < beat_samples:
            # Apply lead-specific polarity
            polarity = self._get_lead_polarity(lead)
            beat[pos:pos + qrs_len] = polarity * qrs
        pos += qrs_len + int(0.08 * self.sampling_rate)  # ST segment
        
        # T wave
        t = self._templates['t_normal']
        t_len = len(t)
        if pos + t_len < beat_samples:
            beat[pos:pos + t_len] = t
        
        return beat
    
    def _get_lead_polarity(self, lead: str) -> float:
        """Get QRS polarity for different leads."""
        # Simplified polarity based on lead axis
        positive_leads = ['I', 'II', 'V4', 'V5', 'V6']
        negative_leads = ['aVR']
        
        if lead in negative_leads:
            return -1.0
        elif lead in positive_leads:
            return 1.0
        else:
            return 0.7  # Mixed polarity
