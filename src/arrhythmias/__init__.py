"""
Arrhythmias Module - 54 Cardiac Arrhythmia Types.

Complete classification based on ESC/ACC guidelines:
- Supraventricular: Bradyarrhythmias (6), Tachyarrhythmias (14), Other (10)
- Ventricular: 16 types
- Special Phenomena: 8 types
"""

from src.arrhythmias.types import ArrhythmiaType
from src.arrhythmias.config import ArrhythmiaConfig, get_arrhythmia_config
from src.arrhythmias.registry import ARRHYTHMIA_REGISTRY

__all__ = [
    "ArrhythmiaType",
    "ArrhythmiaConfig", 
    "get_arrhythmia_config",
    "ARRHYTHMIA_REGISTRY"
]
