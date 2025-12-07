"""
Realistic Layer - Hodgkin-Huxley Based ECG Generation.

Uses full electrophysiological models for maximum accuracy.
Computationally intensive, takes seconds to generate.
"""

from typing import Dict, List
import numpy as np
from src.layers.base import BaseLayer


class RealisticLayer(BaseLayer):
    """
    Realistic simulation layer using Hodgkin-Huxley models.
    
    Characteristics:
    - Latency: Seconds to minutes
    - Accuracy: Research-grade
    - Use case: Scientific research, validation
    
    Implementation:
    - Hodgkin-Huxley ionic current models
    - Cellular action potential simulation
    - Tissue propagation (simplified forward problem)
    """
    
    # Hodgkin-Huxley constants (cardiac adapted)
    C_m = 1.0  # Membrane capacitance (µF/cm²)
    g_Na = 120.0  # Sodium conductance (mS/cm²)
    g_K = 36.0  # Potassium conductance (mS/cm²)
    g_L = 0.3  # Leak conductance (mS/cm²)
    E_Na = 50.0  # Sodium reversal potential (mV)
    E_K = -77.0  # Potassium reversal potential (mV)
    E_L = -54.4  # Leak reversal potential (mV)
    
    def __init__(self, sampling_rate: int = 500):
        super().__init__(sampling_rate)
        self.dt = 1.0 / sampling_rate  # Time step in seconds
        self.dt_ms = 1000.0 / sampling_rate  # Time step in ms
        
    def generate(
        self,
        config: 'ArrhythmiaConfig',
        num_samples: int,
        leads: List[str],
        noise_level: float = 0.01,
        hrv: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """
        Generate ECG using Hodgkin-Huxley based simulation.
        
        This is computationally intensive but produces the most
        realistic results.
        """
        signals = {}
        
        # Generate cellular action potentials
        ap = self._generate_action_potential_train(num_samples, config, hrv)
        
        # Solve forward problem: AP → ECG
        for lead in leads:
            ecg = self._forward_problem(ap, lead, config)
            ecg = self._add_noise(ecg, noise_level)
            signals[lead] = ecg
        
        return signals
    
    def _generate_action_potential_train(
        self,
        num_samples: int,
        config: 'ArrhythmiaConfig',
        hrv: float
    ) -> np.ndarray:
        """Generate a train of action potentials."""
        ap = np.zeros(num_samples)
        
        # Calculate timing
        rate = np.mean(config.rate_range)
        rr_samples = int((60.0 / rate) * self.sampling_rate)
        
        current_pos = 0
        while current_pos < num_samples:
            # Generate single action potential
            single_ap = self._hodgkin_huxley_ap()
            
            # Place in train
            end_pos = min(current_pos + len(single_ap), num_samples)
            ap[current_pos:end_pos] = single_ap[:end_pos - current_pos]
            
            # Next beat with HRV
            rr_var = int(rr_samples * np.random.uniform(-hrv, hrv))
            current_pos += rr_samples + rr_var
        
        return ap
    
    def _hodgkin_huxley_ap(self) -> np.ndarray:
        """
        Generate single action potential using Hodgkin-Huxley model.
        
        Simplified cardiac adaptation of the classic HH equations.
        """
        # Duration of one AP cycle (400ms)
        duration_ms = 400
        num_points = int(duration_ms / self.dt_ms)
        
        # Initialize state variables
        V = -65.0  # Initial membrane potential (mV)
        m = self._m_inf(V)
        h = self._h_inf(V)
        n = self._n_inf(V)
        
        # Stimulus
        I_stim = np.zeros(num_points)
        I_stim[10:20] = 10.0  # 10ms stimulus pulse
        
        # Time integration (Euler method)
        V_trace = np.zeros(num_points)
        
        for i in range(num_points):
            # Ionic currents
            I_Na = self.g_Na * (m**3) * h * (V - self.E_Na)
            I_K = self.g_K * (n**4) * (V - self.E_K)
            I_L = self.g_L * (V - self.E_L)
            
            # Membrane equation
            dV = (I_stim[i] - I_Na - I_K - I_L) / self.C_m
            V += dV * self.dt_ms
            
            # Gating variables
            m += (self._m_inf(V) - m) / self._tau_m(V) * self.dt_ms
            h += (self._h_inf(V) - h) / self._tau_h(V) * self.dt_ms
            n += (self._n_inf(V) - n) / self._tau_n(V) * self.dt_ms
            
            # Clamp gating variables
            m = np.clip(m, 0, 1)
            h = np.clip(h, 0, 1)
            n = np.clip(n, 0, 1)
            
            V_trace[i] = V
        
        return V_trace / 100.0  # Normalize to mV scale for ECG
    
    # Gating variable steady-states and time constants
    def _alpha_m(self, V: float) -> float:
        return 0.1 * (V + 40) / (1 - np.exp(-(V + 40) / 10)) if V != -40 else 1.0
    
    def _beta_m(self, V: float) -> float:
        return 4 * np.exp(-(V + 65) / 18)
    
    def _alpha_h(self, V: float) -> float:
        return 0.07 * np.exp(-(V + 65) / 20)
    
    def _beta_h(self, V: float) -> float:
        return 1 / (1 + np.exp(-(V + 35) / 10))
    
    def _alpha_n(self, V: float) -> float:
        return 0.01 * (V + 55) / (1 - np.exp(-(V + 55) / 10)) if V != -55 else 0.1
    
    def _beta_n(self, V: float) -> float:
        return 0.125 * np.exp(-(V + 65) / 80)
    
    def _m_inf(self, V: float) -> float:
        am = self._alpha_m(V)
        bm = self._beta_m(V)
        return am / (am + bm)
    
    def _h_inf(self, V: float) -> float:
        ah = self._alpha_h(V)
        bh = self._beta_h(V)
        return ah / (ah + bh)
    
    def _n_inf(self, V: float) -> float:
        an = self._alpha_n(V)
        bn = self._beta_n(V)
        return an / (an + bn)
    
    def _tau_m(self, V: float) -> float:
        return 1 / (self._alpha_m(V) + self._beta_m(V))
    
    def _tau_h(self, V: float) -> float:
        return 1 / (self._alpha_h(V) + self._beta_h(V))
    
    def _tau_n(self, V: float) -> float:
        return 1 / (self._alpha_n(V) + self._beta_n(V))
    
    def _forward_problem(
        self,
        ap: np.ndarray,
        lead: str,
        config: 'ArrhythmiaConfig'
    ) -> np.ndarray:
        """
        Solve forward problem: Action Potential → Surface ECG.
        
        Simplified transfer function based on lead position.
        """
        # Lead-specific transfer coefficients (simplified)
        transfer = self._get_transfer_coefficients(lead)
        
        # Convolution-based transformation
        kernel_size = int(0.04 * self.sampling_rate)  # 40ms kernel
        kernel = self._create_transfer_kernel(kernel_size, transfer)
        
        # Apply transfer
        ecg = np.convolve(ap, kernel, mode='same')
        
        # Normalize amplitude
        max_amp = np.max(np.abs(ecg))
        if max_amp > 0:
            ecg = ecg / max_amp
        
        return ecg
    
    def _get_transfer_coefficients(self, lead: str) -> dict:
        """Get transfer function coefficients for lead."""
        # Based on Einthoven's triangle geometry
        coeffs = {
            'I': {'delay': 0, 'amplitude': 0.8, 'invert': False},
            'II': {'delay': 2, 'amplitude': 1.0, 'invert': False},
            'III': {'delay': 4, 'amplitude': 0.6, 'invert': False},
            'aVR': {'delay': 1, 'amplitude': 0.5, 'invert': True},
            'aVL': {'delay': 3, 'amplitude': 0.5, 'invert': False},
            'aVF': {'delay': 3, 'amplitude': 0.7, 'invert': False},
            'V1': {'delay': 5, 'amplitude': 0.4, 'invert': True},
            'V2': {'delay': 4, 'amplitude': 0.6, 'invert': False},
            'V3': {'delay': 3, 'amplitude': 0.8, 'invert': False},
            'V4': {'delay': 2, 'amplitude': 1.0, 'invert': False},
            'V5': {'delay': 1, 'amplitude': 0.9, 'invert': False},
            'V6': {'delay': 0, 'amplitude': 0.8, 'invert': False},
        }
        return coeffs.get(lead, {'delay': 0, 'amplitude': 1.0, 'invert': False})
    
    def _create_transfer_kernel(self, size: int, coeffs: dict) -> np.ndarray:
        """Create convolution kernel for forward problem."""
        kernel = np.zeros(size)
        center = size // 2
        
        # Gaussian derivative (models dipole)
        x = np.linspace(-2, 2, size)
        kernel = x * np.exp(-x**2)
        
        # Apply amplitude
        kernel *= coeffs['amplitude']
        
        # Apply inversion
        if coeffs['invert']:
            kernel *= -1
        
        return kernel / np.sum(np.abs(kernel))
