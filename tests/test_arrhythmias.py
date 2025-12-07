"""
Unit tests for arrhythmia types and configurations.
"""

import pytest
from src.arrhythmias import ArrhythmiaType, ArrhythmiaConfig, get_arrhythmia_config


class TestArrhythmiaType:
    """Tests for ArrhythmiaType enumeration."""
    
    def test_total_arrhythmia_count(self):
        """Verify we have at least 54 arrhythmia types."""
        count = ArrhythmiaType.count()
        assert count['total'] >= 54, f"Expected 54+ arrhythmias, got {count['total']}"
    
    def test_supraventricular_categories(self):
        """Test supraventricular arrhythmia categories."""
        supra = ArrhythmiaType.get_supraventricular()
        assert len(supra) >= 20, "Should have at least 20 supraventricular arrhythmias"
    
    def test_ventricular_categories(self):
        """Test ventricular arrhythmia categories."""
        vent = ArrhythmiaType.get_ventricular()
        assert len(vent) >= 10, "Should have at least 10 ventricular arrhythmias"
    
    def test_special_phenomena(self):
        """Test special phenomena categories."""
        special = ArrhythmiaType.get_special()
        assert len(special) >= 5, "Should have at least 5 special phenomena"
    
    def test_atrial_fibrillation_exists(self):
        """Verify atrial fibrillation is properly defined."""
        assert hasattr(ArrhythmiaType, 'SUPRA_TACHY_ATRIAL_FIBRILLATION')
        af = ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION
        assert af.value == "atrial_fibrillation"
    
    def test_ventricular_fibrillation_exists(self):
        """Verify ventricular fibrillation types exist."""
        assert hasattr(ArrhythmiaType, 'VENT_VF_COARSE')
        assert hasattr(ArrhythmiaType, 'VENT_VF_FINE')


class TestArrhythmiaConfig:
    """Tests for ArrhythmiaConfig dataclass."""
    
    def test_normal_sinus_config(self):
        """Test normal sinus rhythm configuration."""
        config = get_arrhythmia_config(ArrhythmiaType.NORMAL_SINUS)
        
        assert config.rate_range == (60, 100)
        assert config.rate_regularity == "regular"
        assert config.qrs_duration == (80, 100)
        assert config.mechanism == "normal"
    
    def test_af_config(self):
        """Test atrial fibrillation configuration."""
        config = get_arrhythmia_config(ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION)
        
        assert config.rate_regularity == "irregular"
        assert config.mechanism == "reentry"
        assert config.p_wave.morphology == "absent"
    
    def test_vf_config_is_life_threatening(self):
        """Test that VF is marked as life threatening."""
        config = get_arrhythmia_config(ArrhythmiaType.VENT_VF_COARSE)
        
        assert config.is_life_threatening is True
        assert config.urgency == "critical"
    
    def test_config_to_dict(self):
        """Test configuration serialization."""
        config = get_arrhythmia_config(ArrhythmiaType.NORMAL_SINUS)
        data = config.to_dict()
        
        assert 'name' in data
        assert 'rate_range' in data
        assert 'mechanism' in data
    
    def test_unknown_arrhythmia_returns_default(self):
        """Test that unknown arrhythmias return a default config."""
        # This tests arrhythmias not yet fully configured
        config = get_arrhythmia_config(ArrhythmiaType.SUPRA_OTHER_PAC)
        assert config is not None
        assert config.name is not None


class TestArrhythmiaClassification:
    """Tests for arrhythmia classification methods."""
    
    def test_bradyarrhythmias_classification(self):
        """Test bradyarrhythmia identification."""
        brady = ArrhythmiaType.get_bradyarrhythmias()
        
        # Should include sinus bradycardia
        assert ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA in brady
        
        # Should include complete block
        assert ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3 in brady
    
    def test_tachyarrhythmias_classification(self):
        """Test tachyarrhythmia identification."""
        tachy = ArrhythmiaType.get_tachyarrhythmias()
        
        # Should include AF
        assert ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION in tachy
        
        # Should include VT
        assert ArrhythmiaType.VENT_VT_MONO in tachy


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
