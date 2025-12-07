"""
Arrhythmia Types Enumeration.

Complete enumeration of 54 cardiac arrhythmias organized by category.
"""

from enum import Enum


class ArrhythmiaType(Enum):
    """
    Comprehensive enumeration of 54 cardiac arrhythmias.
    
    Categories:
    - SUPRA_BRADY_*: Supraventricular bradyarrhythmias (6)
    - SUPRA_TACHY_*: Supraventricular tachyarrhythmias (14)
    - SUPRA_OTHER_*: Other supraventricular (10)
    - VENT_*: Ventricular arrhythmias (16)
    - SPECIAL_*: Special phenomena (8)
    """
    
    # ========================================
    # SUPRAVENTRICULAR BRADYARRHYTHMIAS (6)
    # ========================================
    SUPRA_BRADY_SINUS_BRADYCARDIA = "sinus_bradycardia"
    SUPRA_BRADY_SICK_SINUS = "sick_sinus_syndrome"
    SUPRA_BRADY_AV_BLOCK_1 = "av_block_first_degree"
    SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH = "av_block_2_wenckebach"
    SUPRA_BRADY_AV_BLOCK_2_MOBITZ = "av_block_2_mobitz"
    SUPRA_BRADY_AV_BLOCK_3 = "av_block_complete"
    
    # ========================================
    # SUPRAVENTRICULAR TACHYARRHYTHMIAS (14)
    # ========================================
    SUPRA_TACHY_SINUS_TACHYCARDIA = "sinus_tachycardia"
    SUPRA_TACHY_ATRIAL_TACHYCARDIA = "atrial_tachycardia"
    SUPRA_TACHY_ATRIAL_FLUTTER = "atrial_flutter"
    SUPRA_TACHY_ATRIAL_FIBRILLATION = "atrial_fibrillation"
    SUPRA_TACHY_AVNRT = "avnrt"
    SUPRA_TACHY_AVRT = "avrt"
    SUPRA_TACHY_WPW = "wpw_syndrome"
    SUPRA_TACHY_PSVT = "psvt"
    SUPRA_TACHY_MAT = "multifocal_atrial_tachy"
    SUPRA_TACHY_FOCAL_AT = "focal_atrial_tachy"
    SUPRA_TACHY_INTRA_ATRIAL_REENTRY = "intra_atrial_reentry"
    SUPRA_TACHY_SINUS_NODE_REENTRY = "sinus_node_reentry"
    SUPRA_TACHY_ECTOPIC_ATRIAL = "ectopic_atrial_rhythm"
    SUPRA_TACHY_ATRIAL_FLUTTER_ATYPICAL = "atypical_atrial_flutter"
    
    # ========================================
    # OTHER SUPRAVENTRICULAR (10)
    # ========================================
    SUPRA_OTHER_PAC = "premature_atrial_contraction"
    SUPRA_OTHER_PJC = "premature_junctional_contraction"
    SUPRA_OTHER_JUNCTIONAL_ESCAPE = "junctional_escape_rhythm"
    SUPRA_OTHER_JUNCTIONAL_TACHY = "junctional_tachycardia"
    SUPRA_OTHER_JET = "junctional_ectopic_tachy"
    SUPRA_OTHER_WANDERING_PACEMAKER = "wandering_atrial_pacemaker"
    SUPRA_OTHER_SINUS_ARRHYTHMIA = "sinus_arrhythmia"
    SUPRA_OTHER_SINUS_PAUSE = "sinus_pause"
    SUPRA_OTHER_SINUS_ARREST = "sinus_arrest"
    SUPRA_OTHER_SINOATRIAL_BLOCK = "sinoatrial_exit_block"
    
    # ========================================
    # VENTRICULAR ARRHYTHMIAS (16)
    # ========================================
    VENT_PVC = "premature_ventricular_contraction"
    VENT_PVC_BIGEMINY = "pvc_bigeminy"
    VENT_PVC_TRIGEMINY = "pvc_trigeminy"
    VENT_PVC_COUPLET = "pvc_couplet"
    VENT_PVC_TRIPLET = "pvc_triplet"
    VENT_AIVR = "accelerated_idioventricular_rhythm"
    VENT_ESCAPE = "ventricular_escape_rhythm"
    VENT_VT_MONO = "ventricular_tachycardia_monomorphic"
    VENT_VT_POLY = "ventricular_tachycardia_polymorphic"
    VENT_VT_SUSTAINED = "ventricular_tachycardia_sustained"
    VENT_VT_NONSUSTAINED = "ventricular_tachycardia_nonsustained"
    VENT_TORSADES = "torsades_de_pointes"
    VENT_VF_COARSE = "ventricular_fibrillation_coarse"
    VENT_VF_FINE = "ventricular_fibrillation_fine"
    VENT_ASYSTOLE = "ventricular_asystole"
    VENT_IDIOVENTRICULAR = "idioventricular_rhythm"
    
    # ========================================
    # SPECIAL PHENOMENA (8)
    # ========================================
    SPECIAL_PARASYSTOLE = "parasystole"
    SPECIAL_FUSION_BEAT = "fusion_beat"
    SPECIAL_CAPTURE_BEAT = "capture_beat"
    SPECIAL_R_ON_T = "r_on_t_phenomenon"
    SPECIAL_ASHMAN = "ashman_phenomenon"
    SPECIAL_CONCEALED_CONDUCTION = "concealed_conduction"
    SPECIAL_AV_DISSOCIATION = "av_dissociation"
    SPECIAL_BRUGADA_PATTERN = "brugada_pattern"
    
    # ========================================
    # NORMAL RHYTHM (baseline)
    # ========================================
    NORMAL_SINUS = "normal_sinus_rhythm"
    
    @classmethod
    def get_supraventricular(cls) -> list:
        """Get all supraventricular arrhythmias."""
        return [a for a in cls if a.name.startswith('SUPRA_')]
    
    @classmethod
    def get_ventricular(cls) -> list:
        """Get all ventricular arrhythmias."""
        return [a for a in cls if a.name.startswith('VENT_')]
    
    @classmethod
    def get_special(cls) -> list:
        """Get all special phenomena."""
        return [a for a in cls if a.name.startswith('SPECIAL_')]
    
    @classmethod
    def get_bradyarrhythmias(cls) -> list:
        """Get all bradyarrhythmias."""
        return [a for a in cls if 'BRADY' in a.name or a in [
            cls.VENT_ESCAPE, cls.VENT_IDIOVENTRICULAR, cls.VENT_ASYSTOLE
        ]]
    
    @classmethod
    def get_tachyarrhythmias(cls) -> list:
        """Get all tachyarrhythmias."""
        return [a for a in cls if 'TACHY' in a.name or 'VT' in a.name or 'VF' in a.name]
    
    @classmethod
    def count(cls) -> dict:
        """Get count by category."""
        return {
            'supraventricular': len(cls.get_supraventricular()),
            'ventricular': len(cls.get_ventricular()),
            'special': len(cls.get_special()),
            'total': len(cls) - 1  # Exclude NORMAL_SINUS
        }
