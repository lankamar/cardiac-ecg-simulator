"""
Tests for ECG templates and Simple Layer v1.1.
"""

import pytest
import numpy as np
from src.arrhythmias.types import ArrhythmiaType
from src.data.arrhythmia_templates import (
    ECGTemplate, WaveTemplate, 
    get_template, TEMPLATES, 
    list_implemented_templates, get_template_stats
)
from src.layers.simple_layer import SimpleLayer


class TestWaveTemplate:
    """Tests for WaveTemplate generation."""
    
    def test_gaussian_wave(self):
        """Test gaussian wave generation."""
        wave = WaveTemplate(amplitude=1.0, duration_ms=80, shape='gaussian')
        samples = wave.generate(sampling_rate=500)
        
        assert len(samples) == 40  # 80ms at 500Hz
        assert np.max(samples) <= 1.0
        assert np.max(samples) > 0.9  # Peak should be close to amplitude
    
    def test_qrs_template(self):
        """Test QRS complex generation."""
        wave = WaveTemplate(amplitude=1.0, duration_ms=80, shape='qrs')
        samples = wave.generate(sampling_rate=500)
        
        assert len(samples) == 40
        # QRS should have both positive and negative components
        assert np.max(samples) > 0
        assert np.min(samples) < 0
    
    def test_wide_qrs_template(self):
        """Test wide QRS for ventricular arrhythmias."""
        wave = WaveTemplate(amplitude=1.5, duration_ms=140, shape='wide_qrs')
        samples = wave.generate(sampling_rate=500)
        
        # Wide QRS should be longer
        assert len(samples) > 50
        assert np.max(samples) > 1.0  # Higher amplitude
    
    def test_polarity_inversion(self):
        """Test negative polarity."""
        wave_pos = WaveTemplate(amplitude=1.0, duration_ms=80, shape='gaussian', polarity=1)
        wave_neg = WaveTemplate(amplitude=1.0, duration_ms=80, shape='gaussian', polarity=-1)
        
        pos_samples = wave_pos.generate()
        neg_samples = wave_neg.generate()
        
        assert np.max(pos_samples) > 0
        assert np.max(neg_samples) < 0


class TestECGTemplate:
    """Tests for complete ECG templates."""
    
    def test_normal_sinus_template(self):
        """Test normal sinus rhythm template."""
        template = get_template(ArrhythmiaType.NORMAL_SINUS)
        
        assert template.name == "Normal Sinus Rhythm"
        assert template.p_wave is not None
        assert template.qrs_complex is not None
        assert template.t_wave is not None
        assert template.rate_bpm == (60, 100)
        assert template.regularity == 'regular'
    
    def test_afib_template_no_p_wave(self):
        """Test AFib has no P wave."""
        template = get_template(ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION)
        
        assert template.p_wave is None  # Key feature of AFib
        assert template.baseline == 'fibrillatory'
        assert template.regularity == 'chaotic'
        assert template.rr_variability >= 0.25  # High variability
    
    def test_flutter_template(self):
        """Test atrial flutter template."""
        template = get_template(ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER)
        
        assert template.p_wave is None  # Flutter waves instead
        assert template.baseline == 'flutter'  # Sawtooth pattern
    
    def test_vt_wide_qrs(self):
        """Test VT has wide QRS."""
        template = get_template(ArrhythmiaType.VENT_VT_MONO)
        
        assert template.qrs_complex.duration_ms >= 120  # Wide QRS
        assert template.qrs_complex.shape == 'wide_qrs'
    
    def test_vf_chaotic(self):
        """Test VF is completely chaotic."""
        template = get_template(ArrhythmiaType.VENT_VF_COARSE)
        
        assert template.baseline == 'chaotic'
        assert template.regularity == 'chaotic'
    
    def test_asystole_flatline(self):
        """Test asystole is flatline."""
        template = get_template(ArrhythmiaType.VENT_ASYSTOLE)
        
        assert template.rate_bpm == (0, 0)
        assert template.qrs_complex.amplitude == 0
    
    def test_generate_beat(self):
        """Test beat generation from template."""
        template = get_template(ArrhythmiaType.NORMAL_SINUS)
        beat = template.generate_beat(sampling_rate=500, lead='II')
        
        assert len(beat) > 0
        assert np.max(np.abs(beat)) > 0  # Should have some signal


class TestTemplateRegistry:
    """Tests for template registry functions."""
    
    def test_implemented_count(self):
        """Test we have 10 priority arrhythmias."""
        assert len(TEMPLATES) >= 10
    
    def test_list_implemented(self):
        """Test listing implemented templates."""
        names = list_implemented_templates()
        
        assert "Normal Sinus Rhythm" in names
        assert "Atrial Fibrillation" in names
        assert "Monomorphic Ventricular Tachycardia" in names
    
    def test_get_template_stats(self):
        """Test statistics function."""
        stats = get_template_stats()
        
        assert 'implemented' in stats
        assert 'total' in stats
        assert 'coverage' in stats
        assert 'arrhythmias' in stats
        assert stats['implemented'] >= 10
    
    def test_fallback_for_unimplemented(self):
        """Test fallback behavior for unimplemented arrhythmias."""
        # Try to get a template that's not implemented
        template = get_template(ArrhythmiaType.SPECIAL_PARASYSTOLE)
        
        # Should return normal sinus as fallback
        assert template is not None


class TestSimpleLayerGeneration:
    """Tests for SimpleLayer ECG generation."""
    
    @pytest.fixture
    def layer(self):
        return SimpleLayer(sampling_rate=500)
    
    def test_normal_sinus_generation(self, layer):
        """Test normal sinus rhythm generation."""
        signals = layer.generate_from_type(
            ArrhythmiaType.NORMAL_SINUS,
            duration_seconds=5,
            leads=['II'],
            noise_level=0.01
        )
        
        assert 'II' in signals
        assert len(signals['II']) == 2500  # 5s at 500Hz
        assert np.max(np.abs(signals['II'])) > 0.1
    
    def test_afib_irregular_rr(self, layer):
        """Test AFib has irregular RR intervals."""
        signals = layer.generate_from_type(
            ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
            duration_seconds=10,
            leads=['II']
        )
        
        signal = signals['II']
        
        # Find R peaks (approximate)
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(signal, height=0.3, distance=100)
        
        if len(peaks) >= 3:
            rr_intervals = np.diff(peaks)
            rr_variability = np.std(rr_intervals) / np.mean(rr_intervals)
            # AFib should have higher variability than normal
            assert rr_variability > 0.05
    
    def test_vf_chaotic_output(self, layer):
        """Test VF produces chaotic output."""
        signals = layer.generate_from_type(
            ArrhythmiaType.VENT_VF_COARSE,
            duration_seconds=5,
            leads=['II']
        )
        
        signal = signals['II']
        
        # VF should be chaotic - no clear peaks
        assert len(signal) == 2500
        # Should have rapid fluctuations
        crossings = np.sum(np.diff(np.sign(signal)) != 0)
        assert crossings > 500  # Many zero crossings
    
    def test_asystole_flat(self, layer):
        """Test asystole is essentially flat."""
        signals = layer.generate_from_type(
            ArrhythmiaType.VENT_ASYSTOLE,
            duration_seconds=5,
            leads=['II'],
            noise_level=0.001
        )
        
        signal = signals['II']
        
        # Should be nearly flat
        assert np.std(signal) < 0.1
    
    def test_multiple_leads(self, layer):
        """Test generation of multiple leads."""
        leads = ['I', 'II', 'III', 'V1', 'V6']
        signals = layer.generate_from_type(
            ArrhythmiaType.NORMAL_SINUS,
            duration_seconds=5,
            leads=leads
        )
        
        assert len(signals) == 5
        for lead in leads:
            assert lead in signals
            assert len(signals[lead]) == 2500
    
    def test_list_supported_arrhythmias(self):
        """Test listing supported arrhythmias."""
        supported = SimpleLayer.list_supported_arrhythmias()
        
        assert 'normal_sinus_rhythm' in supported
        assert 'atrial_fibrillation' in supported
        assert len(supported) >= 10
    
    def test_coverage_stats(self):
        """Test coverage statistics."""
        stats = SimpleLayer.get_coverage()
        
        assert stats['implemented'] >= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
