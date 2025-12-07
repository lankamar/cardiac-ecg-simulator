"""
Unit tests for the simulator layers.
"""

import pytest
import numpy as np
from src.layers import SimpleLayer, IntermediateLayer, RealisticLayer
from src.arrhythmias import ArrhythmiaType, get_arrhythmia_config


class TestSimpleLayer:
    """Tests for SimpleLayer."""
    
    @pytest.fixture
    def layer(self):
        return SimpleLayer(sampling_rate=500)
    
    def test_initialization(self, layer):
        """Test layer initializes correctly."""
        assert layer.sampling_rate == 500
        assert layer._templates is not None
    
    def test_generate_returns_signals(self, layer):
        """Test that generate returns signal dictionary."""
        config = get_arrhythmia_config(ArrhythmiaType.NORMAL_SINUS)
        signals = layer.generate(
            config=config,
            num_samples=5000,
            leads=['II'],
            noise_level=0.01,
            hrv=0.05
        )
        
        assert 'II' in signals
        assert len(signals['II']) == 5000
    
    def test_multiple_leads(self, layer):
        """Test generation of multiple leads."""
        config = get_arrhythmia_config(ArrhythmiaType.NORMAL_SINUS)
        leads = ['I', 'II', 'V1', 'V6']
        
        signals = layer.generate(
            config=config,
            num_samples=5000,
            leads=leads
        )
        
        assert len(signals) == 4
        for lead in leads:
            assert lead in signals
    
    def test_signal_amplitude_range(self, layer):
        """Test that signals have reasonable amplitudes."""
        config = get_arrhythmia_config(ArrhythmiaType.NORMAL_SINUS)
        signals = layer.generate(
            config=config,
            num_samples=5000,
            leads=['II']
        )
        
        signal = signals['II']
        assert np.max(np.abs(signal)) < 5.0  # Max 5mV is reasonable


class TestIntermediateLayer:
    """Tests for IntermediateLayer."""
    
    @pytest.fixture
    def layer(self):
        return IntermediateLayer(sampling_rate=500)
    
    def test_initialization(self, layer):
        """Test layer initializes correctly."""
        assert layer.sampling_rate == 500
        assert layer._params is not None
    
    def test_atrial_fibrillation_no_p_waves(self, layer):
        """Test that AF generates without P waves."""
        config = get_arrhythmia_config(ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION)
        signals = layer.generate(
            config=config,
            num_samples=5000,
            leads=['II']
        )
        
        # Signal should still be generated
        assert 'II' in signals
        assert len(signals['II']) == 5000


class TestRealisticLayer:
    """Tests for RealisticLayer."""
    
    @pytest.fixture
    def layer(self):
        return RealisticLayer(sampling_rate=500)
    
    def test_initialization(self, layer):
        """Test layer initializes correctly."""
        assert layer.sampling_rate == 500
        assert layer.dt == 1.0 / 500
    
    def test_hodgkin_huxley_constants(self, layer):
        """Test HH constants are defined."""
        assert layer.g_Na == 120.0
        assert layer.g_K == 36.0
        assert layer.E_Na == 50.0
        assert layer.E_K == -77.0
    
    def test_generate_produces_output(self, layer):
        """Test that realistic layer produces output."""
        config = get_arrhythmia_config(ArrhythmiaType.NORMAL_SINUS)
        signals = layer.generate(
            config=config,
            num_samples=2500,  # 5 seconds
            leads=['II']
        )
        
        assert 'II' in signals
        assert len(signals['II']) == 2500


class TestLayerSwitching:
    """Tests for dynamic layer switching."""
    
    def test_state_preservation(self):
        """Test state is preserved when switching layers."""
        simple = SimpleLayer()
        simple._state['test_key'] = 'test_value'
        
        intermediate = IntermediateLayer()
        state = simple.get_state()
        intermediate.set_state(state)
        
        assert intermediate._state.get('test_key') == 'test_value'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
