"""
Main Cardiac ECG Simulator Engine.

This module implements the core simulator with 3 overlapping layers:
- Simple Layer: Lookup tables, <1ms latency
- Intermediate Layer: Parametric models, 10-100ms latency  
- Realistic Layer: Hodgkin-Huxley, seconds of computation
"""

from typing import List, Optional, Union
from enum import Enum
import numpy as np

from src.core.ecg_signal import ECGSignal
from src.arrhythmias import ArrhythmiaType, get_arrhythmia_config
from src.layers import SimpleLayer, IntermediateLayer, RealisticLayer


class LayerType(Enum):
    """Available simulation layers."""
    SIMPLE = "simple"
    INTERMEDIATE = "intermediate"
    REALISTIC = "realistic"


class CardiacSimulator:
    """
    Professional Cardiac ECG Simulator.
    
    Supports 54 arrhythmias with 3 overlapping simulation layers.
    Layers can be switched dynamically based on accuracy requirements.
    
    Example:
        >>> sim = CardiacSimulator(layer='simple')
        >>> ecg = sim.generate(ArrhythmiaType.ATRIAL_FIBRILLATION, duration_seconds=10)
        >>> ecg.plot()
    """
    
    # Standard 12-lead ECG configuration
    STANDARD_LEADS = ['I', 'II', 'III', 'aVR', 'aVL', 'aVF', 
                      'V1', 'V2', 'V3', 'V4', 'V5', 'V6']
    
    # ECG standard parameters
    SAMPLING_RATE = 500  # Hz
    PAPER_SPEED = 25  # mm/s
    AMPLITUDE_SCALE = 10  # mm/mV
    
    def __init__(
        self,
        layer: Union[str, LayerType] = LayerType.SIMPLE,
        sampling_rate: int = 500,
        leads: Optional[List[str]] = None
    ):
        """
        Initialize the cardiac simulator.
        
        Args:
            layer: Simulation layer to use ('simple', 'intermediate', 'realistic')
            sampling_rate: ECG sampling rate in Hz (default: 500)
            leads: List of leads to generate (default: all 12 leads)
        """
        self.sampling_rate = sampling_rate
        self.leads = leads or self.STANDARD_LEADS
        
        # Initialize layer
        if isinstance(layer, str):
            layer = LayerType(layer.lower())
        self.layer_type = layer
        self._layer = self._create_layer(layer)
        
        # State
        self._current_arrhythmia = None
    
    def _create_layer(self, layer_type: LayerType):
        """Create the appropriate simulation layer."""
        layer_map = {
            LayerType.SIMPLE: SimpleLayer,
            LayerType.INTERMEDIATE: IntermediateLayer,
            LayerType.REALISTIC: RealisticLayer,
        }
        return layer_map[layer_type](self.sampling_rate)
    
    def switch_layer(self, new_layer: Union[str, LayerType]) -> None:
        """
        Dynamically switch to a different simulation layer.
        
        The new layer takes over from the current state, maintaining
        continuity in the ECG signal.
        
        Args:
            new_layer: Target layer to switch to
        """
        if isinstance(new_layer, str):
            new_layer = LayerType(new_layer.lower())
        
        # Preserve state from current layer
        current_state = self._layer.get_state()
        
        # Create new layer and restore state
        self.layer_type = new_layer
        self._layer = self._create_layer(new_layer)
        self._layer.set_state(current_state)
    
    def generate(
        self,
        arrhythmia: ArrhythmiaType,
        duration_seconds: float = 10.0,
        leads: Optional[List[str]] = None,
        noise_level: float = 0.01,
        heart_rate_variability: float = 0.05
    ) -> ECGSignal:
        """
        Generate ECG signal for the specified arrhythmia.
        
        Args:
            arrhythmia: Type of arrhythmia to simulate
            duration_seconds: Duration of ECG recording in seconds
            leads: Specific leads to generate (default: all configured leads)
            noise_level: Amount of noise to add (0-1, default: 0.01)
            heart_rate_variability: HRV coefficient (0-1, default: 0.05)
            
        Returns:
            ECGSignal object containing the generated waveforms
        """
        leads = leads or self.leads
        self._current_arrhythmia = arrhythmia
        
        # Get arrhythmia configuration
        config = get_arrhythmia_config(arrhythmia)
        
        # Calculate number of samples
        num_samples = int(duration_seconds * self.sampling_rate)
        
        # Generate using current layer
        signals = self._layer.generate(
            config=config,
            num_samples=num_samples,
            leads=leads,
            noise_level=noise_level,
            hrv=heart_rate_variability
        )
        
        # Create ECGSignal object
        return ECGSignal(
            signals=signals,
            leads=leads,
            sampling_rate=self.sampling_rate,
            arrhythmia=arrhythmia,
            duration=duration_seconds
        )
    
    def generate_continuous(
        self,
        arrhythmia: ArrhythmiaType,
        chunk_duration: float = 1.0
    ):
        """
        Generator for continuous ECG streaming.
        
        Yields ECG chunks continuously, useful for real-time display.
        
        Args:
            arrhythmia: Type of arrhythmia to simulate
            chunk_duration: Duration of each chunk in seconds
            
        Yields:
            ECGSignal chunks
        """
        while True:
            yield self.generate(arrhythmia, duration_seconds=chunk_duration)
    
    @property
    def current_layer(self) -> str:
        """Get the name of the current layer."""
        return self.layer_type.value
    
    @property
    def supported_arrhythmias(self) -> List[ArrhythmiaType]:
        """Get list of all supported arrhythmias."""
        return list(ArrhythmiaType)
    
    def get_arrhythmia_info(self, arrhythmia: ArrhythmiaType) -> dict:
        """Get detailed information about an arrhythmia."""
        return get_arrhythmia_config(arrhythmia).to_dict()
