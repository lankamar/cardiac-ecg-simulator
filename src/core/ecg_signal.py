"""
ECG Signal Data Structure.

Represents a generated ECG signal with all metadata and utilities.
"""

from typing import List, Dict, Optional
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class ECGSignal:
    """
    Container for ECG signal data.
    
    Attributes:
        signals: Dictionary mapping lead names to signal arrays
        leads: List of lead names in order
        sampling_rate: Sampling rate in Hz
        arrhythmia: The arrhythmia type that was simulated
        duration: Duration in seconds
    """
    signals: Dict[str, np.ndarray]
    leads: List[str]
    sampling_rate: int
    arrhythmia: 'ArrhythmiaType'
    duration: float
    
    @property
    def time_axis(self) -> np.ndarray:
        """Get time axis in seconds."""
        num_samples = len(next(iter(self.signals.values())))
        return np.linspace(0, self.duration, num_samples)
    
    @property
    def num_samples(self) -> int:
        """Get total number of samples."""
        return len(next(iter(self.signals.values())))
    
    def get_lead(self, lead: str) -> np.ndarray:
        """Get signal for a specific lead."""
        if lead not in self.signals:
            raise ValueError(f"Lead {lead} not found. Available: {list(self.signals.keys())}")
        return self.signals[lead]
    
    def plot(
        self,
        leads: Optional[List[str]] = None,
        figsize: tuple = (15, 10),
        grid: bool = True,
        title: Optional[str] = None
    ) -> plt.Figure:
        """
        Plot ECG signals with standard ECG paper appearance.
        
        Args:
            leads: Specific leads to plot (default: all)
            figsize: Figure size in inches
            grid: Whether to show ECG grid
            title: Plot title (default: arrhythmia name)
            
        Returns:
            matplotlib Figure object
        """
        leads = leads or self.leads
        num_leads = len(leads)
        
        fig, axes = plt.subplots(num_leads, 1, figsize=figsize, sharex=True)
        if num_leads == 1:
            axes = [axes]
        
        time = self.time_axis
        
        for i, (ax, lead) in enumerate(zip(axes, leads)):
            signal = self.signals[lead]
            
            # Plot signal
            ax.plot(time, signal, 'k-', linewidth=0.8)
            
            # Configure appearance
            ax.set_ylabel(lead, fontsize=10, rotation=0, labelpad=20)
            ax.set_ylim(-2, 2)  # mV range
            
            if grid:
                # ECG paper grid
                ax.grid(True, which='major', color='#ff9999', linewidth=0.5)
                ax.grid(True, which='minor', color='#ffcccc', linewidth=0.25)
                ax.minorticks_on()
            
            # Remove spines except left
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        
        axes[-1].set_xlabel('Time (seconds)', fontsize=12)
        
        # Title
        title = title or f"ECG: {self.arrhythmia.value}"
        fig.suptitle(title, fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def save(
        self,
        filepath: str,
        format: str = 'png',
        dpi: int = 150,
        **plot_kwargs
    ) -> None:
        """
        Save ECG plot to file.
        
        Args:
            filepath: Output file path
            format: Image format (png, pdf, svg)
            dpi: Resolution in dots per inch
            **plot_kwargs: Additional arguments for plot()
        """
        fig = self.plot(**plot_kwargs)
        fig.savefig(filepath, format=format, dpi=dpi, bbox_inches='tight')
        plt.close(fig)
    
    def to_numpy(self) -> np.ndarray:
        """
        Convert to numpy array.
        
        Returns:
            2D array of shape (num_leads, num_samples)
        """
        return np.array([self.signals[lead] for lead in self.leads])
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            'signals': {k: v.tolist() for k, v in self.signals.items()},
            'leads': self.leads,
            'sampling_rate': self.sampling_rate,
            'arrhythmia': self.arrhythmia.value,
            'duration': self.duration
        }
    
    def get_intervals(self) -> dict:
        """
        Calculate ECG intervals from lead II.
        
        Returns:
            Dictionary with RR, PR, QRS, QT intervals in ms
        """
        # TODO: Implement interval detection algorithm
        return {
            'RR': None,
            'PR': None,
            'QRS': None,
            'QT': None
        }
    
    def detect_peaks(self, lead: str = 'II') -> np.ndarray:
        """
        Detect R-peaks in the signal.
        
        Args:
            lead: Lead to analyze (default: II)
            
        Returns:
            Array of R-peak indices
        """
        from scipy.signal import find_peaks
        
        signal = self.signals[lead]
        peaks, _ = find_peaks(signal, height=0.5, distance=self.sampling_rate * 0.3)
        return peaks
