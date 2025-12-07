"""Data module - ECG waveform templates and lookup tables."""

from src.data.arrhythmia_templates import (
    ECGTemplate,
    get_template,
    TEMPLATES
)

__all__ = ["ECGTemplate", "get_template", "TEMPLATES"]
