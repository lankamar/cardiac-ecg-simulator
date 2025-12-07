"""Cardiac ECG Simulator - Professional ECG simulation with 54 arrhythmias."""

__version__ = "0.1.0"
__author__ = "Lankamar"

from src.core.simulator import CardiacSimulator
from src.arrhythmias import ArrhythmiaType

__all__ = ["CardiacSimulator", "ArrhythmiaType"]
