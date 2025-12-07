"""
Intermediate Layer - Parametric ECG Generation.

Uses parametric models for 10-100ms latency with better accuracy.
Ideal for clinical training applications.
"""

from typing import Dict, List
import numpy as np
from src.layers.base import BaseLayer


class IntermediateLayer(BaseLayer):
    """
    Intermediate simulation layer using parametric models.
    
    Characteristics:
    - Latency: 10-100ms
    - Accuracy: Medium-High
    - Use case: Clinical training, realistic demos
    
    Implementation:
    - Parametric waveform generation
    - Dynamic morphology adjustment
    - Realistic interval variations
    """
    
    def __init__(self, sampling_rate: int = 500):
        super().__init__(sampling_rate)
        self._params = self._init_params()
    
    def _init_params(self) -> dict:
        """Initialize parametric model parameters."""
        return {
            'p_duration': 0.08,   # seconds
            'pr_interval': 0.16,  # seconds
            'qrs_duration': 0.08, # seconds
            'qt_interval': 0.40,  # seconds
            'p_amplitude': 0.15,  # mV
            'r_amplitude': 1.0,   # mV
            't_amplitude': 0.3,   # mV
        }
    
    def generate(
        self,
        config: 'ArrhythmiaConfig',
        num_samples: int,
        leads: List[str],
        noise_level: float = 0.01,
        hrv: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """
        Generate ECG using parametric models.
        
        More accurate than SimpleLayer but with some latency.
        """
        signals = {}
        
        # Update params based on arrhythmia config
        params = self._update_params_for_arrhythmia(config)
        
        for lead in leads:
            signal = self._generate_lead_signal(
                lead, num_samples, config, params, noise_level, hrv
            )
            signals[lead] = signal
        
        return signals
    
    def _update_params_for_arrhythmia(self, config: 'ArrhythmiaConfig') -> dict:
        """Update parameters based on arrhythmia configuration."""
        params = self._params.copy()
        
        # Adjust for PR interval
        if config.pr_interval:
            params['pr_interval'] = np.mean(config.pr_interval) / 1000.0
        
        # Adjust for QRS duration
        if config.qrs_duration:
            params['qrs_duration'] = np.mean(config.qrs_duration) / 1000.0
        
        # Adjust for P wave morphology
        if hasattr(config, 'p_wave'):
            if config.p_wave.morphology == 'absent':
                params['p_amplitude'] = 0
            elif config.p_wave.morphology == 'inverted':
                params['p_amplitude'] = -abs(config.p_wave.amplitude)
        
        return params
    
    def _generate_lead_signal(
        self,
        lead: str,
        num_samples: int,
        config: 'ArrhythmiaConfig',
        params: dict,
        noise_level: float,
        hrv: float
    ) -> np.ndarray:
        """Generate signal for a specific lead."""
        signal = np.zeros(num_samples)
        
        # Get lead-specific transforms
        lead_transform = self._get_lead_transform(lead)
        
        # Calculate beat positions with appropriate regularity
        beat_positions = self._calculate_beat_positions(
            num_samples, config, hrv
        )
        
        # Generate each beat
        for beat_pos in beat_positions:
            beat = self._generate_parametric_beat(config, params, lead_transform)
            
            # Place beat in signal
            end_pos = min(beat_pos + len(beat), num_samples)
            beat_len = end_pos - beat_pos
            if beat_len > 0:
                signal[beat_pos:end_pos] = beat[:beat_len]
        
        # Add artifacts
        signal = self._add_noise(signal, noise_level)
        signal = self._apply_baseline_wander(signal)
        
        return signal
    
    def _calculate_beat_positions(
        self,
        num_samples: int,
        config: 'ArrhythmiaConfig',
        hrv: float
    ) -> List[int]:
        """Calculate beat positions based on rhythm regularity."""
        rate = np.random.uniform(*config.rate_range)
        base_rr = int((60.0 / rate) * self.sampling_rate)
        
        positions = []
        current_pos = 0
        
        while current_pos < num_samples:
            positions.append(current_pos)
            
            # Apply variability based on rhythm type
            if config.rate_regularity == 'regular':
                variation = hrv * 0.02
            elif config.rate_regularity == 'irregular':
                variation = 0.3  # Large variation for AF, etc.
            else:  # regularly_irregular
                variation = hrv * 0.15
            
            rr_var = int(base_rr * np.random.uniform(-variation, variation))
            current_pos += base_rr + rr_var
        
        return positions
    
    def _generate_parametric_beat(
        self,
        config: 'ArrhythmiaConfig',
        params: dict,
        lead_transform: dict
    ) -> np.ndarray:
        """Generate a single beat using parametric equations."""
        rate = np.mean(config.rate_range)
        rr = 60.0 / rate
        beat_samples = int(rr * self.sampling_rate)
        
        t = np.linspace(0, rr, beat_samples)
        beat = np.zeros(beat_samples)
        
        # P wave (parametric gaussian)
        if params['p_amplitude'] != 0:
            p_center = params['pr_interval'] - params['p_duration'] / 2
            p_sigma = params['p_duration'] / 4
            p_wave = params['p_amplitude'] * np.exp(-((t - p_center)**2) / (2 * p_sigma**2))
            beat += p_wave * lead_transform.get('p_scale', 1.0)
        
        # QRS complex (superposition of gaussians)
        qrs_center = params['pr_interval'] + params['qrs_duration'] / 2
        qrs = self._parametric_qrs(t, qrs_center, params['qrs_duration'], params['r_amplitude'])
        beat += qrs * lead_transform.get('qrs_scale', 1.0)
        
        # T wave
        t_center = qrs_center + 0.2  # ST segment
        t_sigma = 0.06
        t_wave = params['t_amplitude'] * np.exp(-((t - t_center)**2) / (2 * t_sigma**2))
        beat += t_wave * lead_transform.get('t_scale', 1.0)
        
        return beat
    
    def _parametric_qrs(
        self,
        t: np.ndarray,
        center: float,
        duration: float,
        amplitude: float
    ) -> np.ndarray:
        """Generate parametric QRS complex."""
        sigma = duration / 6
        
        # Q wave
        q_center = center - duration / 3
        q = -0.15 * amplitude * np.exp(-((t - q_center)**2) / (2 * (sigma/2)**2))
        
        # R wave
        r = amplitude * np.exp(-((t - center)**2) / (2 * sigma**2))
        
        # S wave
        s_center = center + duration / 3
        s = -0.3 * amplitude * np.exp(-((t - s_center)**2) / (2 * (sigma/2)**2))
        
        return q + r + s
    
    def _get_lead_transform(self, lead: str) -> dict:
        """Get lead-specific transformation parameters."""
        # Based on Einthoven's triangle and precordial lead positions
        transforms = {
            'I': {'p_scale': 1.0, 'qrs_scale': 0.8, 't_scale': 1.0},
            'II': {'p_scale': 1.2, 'qrs_scale': 1.0, 't_scale': 1.1},
            'III': {'p_scale': 0.5, 'qrs_scale': 0.6, 't_scale': 0.5},
            'aVR': {'p_scale': -0.5, 'qrs_scale': -0.5, 't_scale': -0.5},
            'aVL': {'p_scale': 0.6, 'qrs_scale': 0.4, 't_scale': 0.6},
            'aVF': {'p_scale': 0.8, 'qrs_scale': 0.8, 't_scale': 0.7},
            'V1': {'p_scale': 0.6, 'qrs_scale': -0.5, 't_scale': -0.3},
            'V2': {'p_scale': 0.5, 'qrs_scale': 0.2, 't_scale': 0.5},
            'V3': {'p_scale': 0.4, 'qrs_scale': 0.6, 't_scale': 0.7},
            'V4': {'p_scale': 0.3, 'qrs_scale': 0.9, 't_scale': 0.8},
            'V5': {'p_scale': 0.3, 'qrs_scale': 1.0, 't_scale': 0.9},
            'V6': {'p_scale': 0.3, 'qrs_scale': 0.9, 't_scale': 0.9},
        }
        return transforms.get(lead, {'p_scale': 1.0, 'qrs_scale': 1.0, 't_scale': 1.0})
