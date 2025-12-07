"""
Base Layer Abstract Class.

Defines the interface that all simulation layers must implement.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
import numpy as np


class BaseLayer(ABC):
    """
    Abstract base class for simulation layers.
    
    All layers (Simple, Intermediate, Realistic) must implement this interface.
    """
    
    def __init__(self, sampling_rate: int = 500):
        """
        Initialize the layer.
        
        Args:
            sampling_rate: ECG sampling rate in Hz
        """
        self.sampling_rate = sampling_rate
        self._state = {}
    
    @abstractmethod
    def generate(
        self,
        config: 'ArrhythmiaConfig',
        num_samples: int,
        leads: List[str],
        noise_level: float = 0.01,
        hrv: float = 0.05
    ) -> Dict[str, np.ndarray]:
        """
        Generate ECG signals for the given arrhythmia.
        
        Args:
            config: Arrhythmia configuration
            num_samples: Number of samples to generate
            leads: List of leads to generate
            noise_level: Amount of noise (0-1)
            hrv: Heart rate variability coefficient
            
        Returns:
            Dictionary mapping lead names to signal arrays
        """
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """
        Get current layer state for handoff to another layer.
        
        Returns:
            State dictionary
        """
        return self._state.copy()
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """
        Set layer state from another layer's state.
        
        Args:
            state: State dictionary from another layer
        """
        self._state.update(state)
    
    def _add_noise(self, signal: np.ndarray, level: float) -> np.ndarray:
        """Add realistic noise to ECG signal."""
        noise = np.random.normal(0, level * 0.1, signal.shape)
        return signal + noise
    
    def _apply_baseline_wander(self, signal: np.ndarray) -> np.ndarray:
        """Add baseline wander artifact."""
        t = np.arange(len(signal)) / self.sampling_rate
        wander = 0.05 * np.sin(2 * np.pi * 0.1 * t)  # 0.1 Hz wander
        return signal + wander
