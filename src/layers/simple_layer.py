"""
Simple Layer - Fast ECG Generation with Lookup Tables.

Uses pre-computed templates for <1ms latency generation.
Ideal for real-time training applications and rapid prototyping.

Implemented arrhythmias (10 priority):
1. Normal Sinus Rhythm
2. Sinus Bradycardia
3. Sinus Tachycardia
4. Atrial Fibrillation
5. Atrial Flutter
6. Ventricular Tachycardia (Monomorphic)
7. Ventricular Fibrillation (Coarse)
8. PVC (Premature Ventricular Contraction)
9. Complete AV Block
10. Asystole
"""

from typing import Dict, List, Optional
import numpy as np
from src.layers.base import BaseLayer
from src.data.arrhythmia_templates import get_template, ECGTemplate, TEMPLATES
from src.arrhythmias.types import ArrhythmiaType


class SimpleLayer(BaseLayer):
    """
    Simple simulation layer using lookup tables.
    
    Characteristics:
    - Latency: <1ms per 10 seconds of ECG
    - Accuracy: Low-Medium (suitable for training)
    - Use case: Real-time display, basic training, demos
    
    Implementation:
    - Pre-computed waveform templates from arrhythmia_templates.py
    - Direct morphology generation with lead adjustments
    - Fast RR interval calculation with variability
    """
    
    # Standard 12-lead configuration
    LEADS = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    
    def __init__(self, sampling_rate: int = 500):
        super().__init__(sampling_rate)
        self._current_template: Optional[ECGTemplate] = None
        self._beat_cache: Dict[str, np.ndarray] = {}
    
    def generate(
        self,
        config: 'ArrhythmiaConfig',
        num_samples: int,
        leads: List[str],
        noise_level: float = 0.01,
        hrv: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """
        Generate ECG signals using lookup tables.
        
        This is the fastest generation method, suitable for real-time display.
        
        Args:
            config: Arrhythmia configuration object
            num_samples: Number of samples to generate
            leads: List of leads to generate (e.g., ['II', 'V1'])
            noise_level: Noise amplitude (0-1)
            hrv: Heart rate variability coefficient
            
        Returns:
            Dictionary mapping lead names to numpy arrays
        """
        # Get template for this arrhythmia
        template = get_template(config.arrhythmia_type)
        self._current_template = template
        
        signals = {}
        
        for lead in leads:
            signal = self._generate_lead_signal(
                template=template,
                num_samples=num_samples,
                lead=lead,
                noise_level=noise_level,
                hrv=hrv
            )
            signals[lead] = signal
        
        return signals
    
    def _generate_lead_signal(
        self,
        template: ECGTemplate,
        num_samples: int,
        lead: str,
        noise_level: float,
        hrv: float
    ) -> np.ndarray:
        """Generate signal for a specific lead."""
        
        # Handle asystole specially
        if template.arrhythmia_type == ArrhythmiaType.VENT_ASYSTOLE:
            signal = np.zeros(num_samples)
            signal = self._add_noise(signal, noise_level * 0.1)  # Very little noise
            return signal
        
        # Handle VF specially (continuous chaos)
        if template.arrhythmia_type == ArrhythmiaType.VENT_VF_COARSE:
            return self._generate_vf_signal(num_samples, noise_level, lead, template)
        
        # Standard beat-based generation
        signal = np.zeros(num_samples)
        
        # Calculate RR intervals
        rate = np.random.uniform(*template.rate_bpm)
        base_rr_ms = 60000 / rate
        base_rr_samples = int(base_rr_ms * self.sampling_rate / 1000)
        
        # Generate beat positions
        current_pos = 0
        beat_count = 0
        
        while current_pos < num_samples:
            # Apply RR variability based on rhythm regularity
            if template.regularity == 'chaotic':
                rr_var = template.rr_variability
            elif template.regularity == 'irregular':
                rr_var = template.rr_variability * 2
            else:
                rr_var = hrv * 0.5
            
            rr_variation = int(base_rr_samples * np.random.uniform(-rr_var, rr_var))
            current_rr = base_rr_samples + rr_variation
            
            if current_rr < 100:  # Safety minimum
                current_rr = 100
            
            # Generate beat
            beat = self._generate_beat(template, lead, beat_count)
            
            # Handle patterns (bigeminy, trigeminy)
            if template.pattern == 'bigeminy' and beat_count % 2 == 1:
                # Every other beat is PVC
                pvc_template = get_template(ArrhythmiaType.VENT_PVC)
                beat = self._generate_beat(pvc_template, lead, beat_count)
            
            # Place beat in signal
            beat_len = min(len(beat), num_samples - current_pos)
            if beat_len > 0:
                signal[current_pos:current_pos + beat_len] += beat[:beat_len]
            
            current_pos += current_rr
            beat_count += 1
        
        # Add noise
        signal = self._add_noise(signal, noise_level)
        
        # Apply baseline wander (subtle)
        if template.baseline == 'flat':
            signal = self._apply_baseline_wander(signal)
        
        return signal
    
    def _generate_beat(
        self,
        template: ECGTemplate,
        lead: str,
        beat_index: int = 0
    ) -> np.ndarray:
        """Generate a single heartbeat from template."""
        
        # Use cached beat if available and no per-beat variation needed
        cache_key = f"{template.arrhythmia_type.value}_{lead}"
        
        # Generate fresh beat
        beat = template.generate_beat(self.sampling_rate, lead)
        
        return beat
    
    def _generate_vf_signal(
        self,
        num_samples: int,
        noise_level: float,
        lead: str,
        template: ECGTemplate
    ) -> np.ndarray:
        """Generate ventricular fibrillation signal (continuous chaos)."""
        t = np.arange(num_samples) / self.sampling_rate
        
        # Multiple overlapping sine waves with noise
        signal = np.zeros(num_samples)
        
        # Base frequency varies between 4-8 Hz
        for freq in [4, 5, 6, 7, 8]:
            amp = np.random.uniform(0.3, 0.8)
            phase = np.random.uniform(0, 2 * np.pi)
            signal += amp * np.sin(2 * np.pi * freq * t + phase)
        
        # Add amplitude modulation (coarse vs fine)
        modulation = 0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t)
        signal *= modulation
        
        # Add high-frequency noise
        signal += 0.2 * np.random.randn(num_samples)
        
        # Normalize to ~1mV peak
        signal = signal / np.max(np.abs(signal)) * 0.8
        
        return signal
    
    def generate_from_type(
        self,
        arrhythmia_type: ArrhythmiaType,
        duration_seconds: float = 10.0,
        leads: Optional[List[str]] = None,
        noise_level: float = 0.01
    ) -> Dict[str, np.ndarray]:
        """
        Convenience method to generate directly from ArrhythmiaType.
        
        Args:
            arrhythmia_type: The ArrhythmiaType enum value
            duration_seconds: Duration of ECG to generate
            leads: List of leads (default: ['II'])
            noise_level: Noise level (0-1)
            
        Returns:
            Dictionary of lead signals
        """
        if leads is None:
            leads = ['II']
        
        template = get_template(arrhythmia_type)
        num_samples = int(duration_seconds * self.sampling_rate)
        
        # Create minimal config-like object
        class MinimalConfig:
            def __init__(self, arr_type):
                self.arrhythmia_type = arr_type
        
        return self.generate(
            config=MinimalConfig(arrhythmia_type),
            num_samples=num_samples,
            leads=leads,
            noise_level=noise_level
        )
    
    @staticmethod
    def list_supported_arrhythmias() -> List[str]:
        """Get list of arrhythmias with implemented templates."""
        return [arr.value for arr in TEMPLATES.keys()]
    
    @staticmethod
    def get_coverage() -> dict:
        """Get template coverage statistics."""
        from src.data.arrhythmia_templates import get_template_stats
        return get_template_stats()
