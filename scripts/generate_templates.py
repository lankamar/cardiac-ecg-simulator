#!/usr/bin/env python
"""
Template Generator for Cardiac ECG Simulator.

Automatically generates ECG templates for the remaining 44 arrhythmias.
Uses predefined parameters based on clinical literature.

Usage:
    python scripts/generate_templates.py --phase 2
    python scripts/generate_templates.py --all
    python scripts/generate_templates.py --arrhythmia av_block_1
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.arrhythmias.types import ArrhythmiaType
from src.data.arrhythmia_templates import WaveTemplate, ECGTemplate, TEMPLATES


# =============================================================================
# TEMPLATE DEFINITIONS FOR ALL 54 ARRHYTHMIAS
# =============================================================================

@dataclass
class ArrhythmiaSpec:
    """Specification for generating an arrhythmia template."""
    arrhythmia_type: ArrhythmiaType
    name: str
    
    # Wave parameters
    p_wave_present: bool = True
    p_amplitude: float = 0.15
    p_duration_ms: float = 80
    p_shape: str = 'gaussian'
    
    qrs_duration_ms: float = 80
    qrs_amplitude: float = 1.0
    qrs_shape: str = 'qrs'  # 'qrs' or 'wide_qrs'
    
    t_wave_present: bool = True
    t_amplitude: float = 0.3
    t_polarity: int = 1
    
    # Intervals
    pr_interval_ms: float = 160
    qt_interval_ms: float = 400
    
    # Rhythm
    rate_min: int = 60
    rate_max: int = 100
    rr_variability: float = 0.05
    regularity: str = 'regular'  # 'regular', 'irregular', 'chaotic'
    
    # Special
    baseline: str = 'flat'  # 'flat', 'fibrillatory', 'flutter', 'chaotic'
    pattern: Optional[str] = None  # 'bigeminy', 'trigeminy', etc.
    
    # Clinical
    phase: int = 1  # Which implementation phase


# Complete specifications for all 54 arrhythmias
ALL_ARRHYTHMIA_SPECS: List[ArrhythmiaSpec] = [
    
    # =========================================================================
    # PHASE 1: Already implemented (10) - v1.1
    # =========================================================================
    ArrhythmiaSpec(
        ArrhythmiaType.NORMAL_SINUS, "Normal Sinus Rhythm",
        rate_min=60, rate_max=100, phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_BRADY_SINUS_BRADYCARDIA, "Sinus Bradycardia",
        rate_min=35, rate_max=59, phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_SINUS_TACHYCARDIA, "Sinus Tachycardia",
        rate_min=100, rate_max=180, phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION, "Atrial Fibrillation",
        p_wave_present=False, rate_min=60, rate_max=160,
        rr_variability=0.30, regularity='chaotic', baseline='fibrillatory', phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER, "Atrial Flutter",
        p_wave_present=False, rate_min=130, rate_max=150,
        baseline='flutter', phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_VT_MONO, "Monomorphic VT",
        p_wave_present=False, qrs_duration_ms=140, qrs_shape='wide_qrs',
        rate_min=140, rate_max=220, t_polarity=-1, phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_VF_COARSE, "VF Coarse",
        p_wave_present=False, t_wave_present=False,
        rate_min=300, rate_max=500, regularity='chaotic', baseline='chaotic', phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_PVC, "PVC",
        p_wave_present=False, qrs_duration_ms=140, qrs_shape='wide_qrs',
        qrs_amplitude=1.8, t_polarity=-1, phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_3, "Complete AV Block",
        qrs_duration_ms=120, qrs_shape='wide_qrs',
        rate_min=30, rate_max=45, pr_interval_ms=0, phase=1
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_ASYSTOLE, "Asystole",
        p_wave_present=False, t_wave_present=False,
        qrs_amplitude=0, rate_min=0, rate_max=0, phase=1
    ),
    
    # =========================================================================
    # PHASE 2: Blocks & Bradyarrhythmias (6) - v1.2
    # =========================================================================
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_BRADY_SICK_SINUS, "Sick Sinus Syndrome",
        rate_min=30, rate_max=100, rr_variability=0.35,
        regularity='irregular', phase=2
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_1, "AV Block 1st Degree",
        pr_interval_ms=280,  # Prolonged PR > 200ms
        rate_min=50, rate_max=90, phase=2
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_WENCKEBACH, "AV Block 2nd Wenckebach",
        rate_min=40, rate_max=80, pr_interval_ms=200,
        regularity='irregular', pattern='wenckebach', phase=2
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_BRADY_AV_BLOCK_2_MOBITZ, "AV Block 2nd Mobitz II",
        rate_min=30, rate_max=70, qrs_duration_ms=120,
        regularity='irregular', pattern='mobitz', phase=2
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_SINUS_PAUSE, "Sinus Pause",
        rate_min=50, rate_max=80, pattern='pause', phase=2
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_SINOATRIAL_BLOCK, "Sinoatrial Exit Block",
        rate_min=50, rate_max=80, pattern='sa_block', phase=2
    ),
    
    # =========================================================================
    # PHASE 3: SVT Advanced (10) - v1.3
    # =========================================================================
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_AVNRT, "AVNRT",
        p_wave_present=False,  # P hidden in QRS
        rate_min=140, rate_max=220, pr_interval_ms=80, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_AVRT, "AVRT",
        qrs_duration_ms=100, pr_interval_ms=100,  # Short PR
        rate_min=140, rate_max=250, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_WPW, "WPW Syndrome",
        qrs_duration_ms=140, qrs_shape='wide_qrs',  # Delta wave
        pr_interval_ms=100, rate_min=100, rate_max=250, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_PSVT, "PSVT",
        p_wave_present=False, rate_min=150, rate_max=220, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_ATRIAL_TACHYCARDIA, "Atrial Tachycardia",
        p_amplitude=0.12,  # Different P morphology
        rate_min=150, rate_max=250, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_MAT, "Multifocal Atrial Tachycardia",
        p_amplitude=0.15, rate_min=100, rate_max=180,
        regularity='irregular', pattern='mat', phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_ATRIAL_FLUTTER_ATYPICAL, "Atypical Flutter",
        p_wave_present=False, rate_min=120, rate_max=200,
        baseline='flutter', phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_JUNCTIONAL_ESCAPE, "Junctional Escape",
        p_wave_present=False, rate_min=40, rate_max=60, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_JUNCTIONAL_TACHY, "Junctional Tachycardia",
        p_wave_present=False, rate_min=70, rate_max=130, phase=3
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_JET, "JET",
        p_wave_present=False, rate_min=120, rate_max=200, phase=3
    ),
    
    # =========================================================================
    # PHASE 4: Ventricular Advanced (10) - v1.4
    # =========================================================================
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_PVC_BIGEMINY, "PVC Bigeminy",
        pattern='bigeminy', qrs_duration_ms=140, qrs_shape='wide_qrs', phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_PVC_TRIGEMINY, "PVC Trigeminy",
        pattern='trigeminy', qrs_duration_ms=140, qrs_shape='wide_qrs', phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_PVC_COUPLET, "PVC Couplet",
        pattern='couplet', qrs_duration_ms=140, qrs_shape='wide_qrs', phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_PVC_TRIPLET, "PVC Triplet / NSVT",
        pattern='triplet', qrs_duration_ms=140, qrs_shape='wide_qrs',
        rate_min=140, rate_max=200, phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_VT_POLY, "Polymorphic VT",
        p_wave_present=False, qrs_duration_ms=140, qrs_shape='wide_qrs',
        rate_min=100, rate_max=250, regularity='irregular', phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_TORSADES, "Torsades de Pointes",
        p_wave_present=False, qrs_duration_ms=150, qrs_shape='wide_qrs',
        rate_min=200, rate_max=300, pattern='torsades', phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_VT_SUSTAINED, "Sustained VT",
        p_wave_present=False, qrs_duration_ms=140, qrs_shape='wide_qrs',
        rate_min=100, rate_max=250, phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_VF_FINE, "VF Fine",
        p_wave_present=False, t_wave_present=False,
        rate_min=300, rate_max=500, regularity='chaotic',
        baseline='chaotic', qrs_amplitude=0.3, phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_AIVR, "AIVR",
        p_wave_present=False, qrs_duration_ms=140, qrs_shape='wide_qrs',
        rate_min=40, rate_max=110, phase=4
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_IDIOVENTRICULAR, "Idioventricular Rhythm",
        p_wave_present=False, qrs_duration_ms=160, qrs_shape='wide_qrs',
        rate_min=20, rate_max=40, phase=4
    ),
    
    # =========================================================================
    # PHASE 5: Extras & Special Phenomena (18) - v1.5
    # =========================================================================
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_PAC, "PAC",
        p_amplitude=0.12, pattern='premature', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_PJC, "PJC",
        p_wave_present=False, pattern='premature', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_WANDERING_PACEMAKER, "Wandering Pacemaker",
        p_amplitude=0.15, regularity='irregular', pattern='wandering', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_OTHER_SINUS_ARRHYTHMIA, "Sinus Arrhythmia",
        rr_variability=0.15, regularity='irregular', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_ECTOPIC_ATRIAL, "Ectopic Atrial Rhythm",
        p_amplitude=0.12, rate_min=60, rate_max=100, phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_SINUS_NODE_REENTRY, "Sinus Node Reentry",
        rate_min=100, rate_max=150, phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_ESCAPE, "Ventricular Escape",
        p_wave_present=False, qrs_duration_ms=160, qrs_shape='wide_qrs',
        rate_min=20, rate_max=40, pattern='escape', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_FUSION_BEAT, "Fusion Beat",
        qrs_duration_ms=100, pattern='fusion', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_CAPTURE_BEAT, "Capture Beat",
        qrs_duration_ms=80, pattern='capture', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_R_ON_T, "R-on-T Phenomenon",
        pattern='r_on_t', qrs_duration_ms=140, qrs_shape='wide_qrs', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_PARASYSTOLE, "Parasystole",
        pattern='parasystole', qrs_duration_ms=140, phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_ASHMAN, "Ashman Phenomenon",
        pattern='ashman', qrs_duration_ms=120, phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_CONCEALED_CONDUCTION, "Concealed Conduction",
        pattern='concealed', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_AV_DISSOCIATION, "AV Dissociation",
        pr_interval_ms=0, pattern='dissociation', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SPECIAL_BRUGADA_PATTERN, "Brugada Pattern",
        pattern='brugada', phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_INTRA_ATRIAL_REENTRY, "Intra-atrial Reentry",
        rate_min=130, rate_max=200, phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.SUPRA_TACHY_FOCAL_AT, "Focal AT",
        p_amplitude=0.12, rate_min=150, rate_max=250, phase=5
    ),
    ArrhythmiaSpec(
        ArrhythmiaType.VENT_VT_NONSUSTAINED, "NSVT",
        p_wave_present=False, qrs_duration_ms=140, qrs_shape='wide_qrs',
        rate_min=100, rate_max=250, pattern='nsvt', phase=5
    ),
]


def spec_to_template(spec: ArrhythmiaSpec) -> ECGTemplate:
    """Convert ArrhythmiaSpec to ECGTemplate."""
    
    # P wave
    p_wave = None
    if spec.p_wave_present:
        p_wave = WaveTemplate(
            amplitude=spec.p_amplitude,
            duration_ms=spec.p_duration_ms,
            shape=spec.p_shape
        )
    
    # QRS complex
    qrs_complex = WaveTemplate(
        amplitude=spec.qrs_amplitude,
        duration_ms=spec.qrs_duration_ms,
        shape=spec.qrs_shape
    )
    
    # T wave
    t_wave = None
    if spec.t_wave_present:
        t_wave = WaveTemplate(
            amplitude=spec.t_amplitude,
            duration_ms=160,
            shape='gaussian',
            polarity=spec.t_polarity
        )
    
    # Create template
    return ECGTemplate(
        name=spec.name,
        arrhythmia_type=spec.arrhythmia_type,
        p_wave=p_wave,
        qrs_complex=qrs_complex,
        t_wave=t_wave,
        pr_interval=spec.pr_interval_ms,
        qt_interval=spec.qt_interval_ms,
        rate_bpm=(spec.rate_min, spec.rate_max),
        rr_variability=spec.rr_variability,
        regularity=spec.regularity,
        pattern=spec.pattern,
        baseline=spec.baseline
    )


def generate_templates_for_phase(phase: int) -> Dict[ArrhythmiaType, ECGTemplate]:
    """Generate templates for a specific phase."""
    templates = {}
    for spec in ALL_ARRHYTHMIA_SPECS:
        if spec.phase == phase:
            templates[spec.arrhythmia_type] = spec_to_template(spec)
    return templates


def generate_all_templates() -> Dict[ArrhythmiaType, ECGTemplate]:
    """Generate all 54 arrhythmia templates."""
    templates = {}
    for spec in ALL_ARRHYTHMIA_SPECS:
        templates[spec.arrhythmia_type] = spec_to_template(spec)
    return templates


def generate_python_code(templates: Dict[ArrhythmiaType, ECGTemplate]) -> str:
    """Generate Python code for templates."""
    lines = [
        '"""Auto-generated arrhythmia templates."""',
        '',
        'from src.data.arrhythmia_templates import ECGTemplate, WaveTemplate',
        'from src.arrhythmias.types import ArrhythmiaType',
        '',
        'GENERATED_TEMPLATES = {'
    ]
    
    for arr_type, template in templates.items():
        lines.append(f'    ArrhythmiaType.{arr_type.name}: ECGTemplate(')
        lines.append(f'        name="{template.name}",')
        lines.append(f'        arrhythmia_type=ArrhythmiaType.{arr_type.name},')
        
        if template.p_wave:
            lines.append(f'        p_wave=WaveTemplate({template.p_wave.amplitude}, {template.p_wave.duration_ms}, "{template.p_wave.shape}"),')
        else:
            lines.append('        p_wave=None,')
        
        lines.append(f'        qrs_complex=WaveTemplate({template.qrs_complex.amplitude}, {template.qrs_complex.duration_ms}, "{template.qrs_complex.shape}"),')
        
        if template.t_wave:
            lines.append(f'        t_wave=WaveTemplate({template.t_wave.amplitude}, {template.t_wave.duration_ms}, "{template.t_wave.shape}", polarity={template.t_wave.polarity}),')
        else:
            lines.append('        t_wave=None,')
        
        lines.append(f'        rate_bpm={template.rate_bpm},')
        lines.append(f'        rr_variability={template.rr_variability},')
        lines.append(f'        regularity="{template.regularity}",')
        lines.append(f'        baseline="{template.baseline}",')
        lines.append('    ),')
    
    lines.append('}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate ECG arrhythmia templates')
    parser.add_argument('--phase', type=int, help='Generate templates for specific phase (1-5)')
    parser.add_argument('--all', action='store_true', help='Generate all 54 templates')
    parser.add_argument('--output', type=str, default=None, help='Output file path')
    parser.add_argument('--list', action='store_true', help='List all arrhythmias by phase')
    
    args = parser.parse_args()
    
    if args.list:
        for phase in range(1, 6):
            specs = [s for s in ALL_ARRHYTHMIA_SPECS if s.phase == phase]
            print(f"\n📦 PHASE {phase} ({len(specs)} arrhythmias):")
            for spec in specs:
                status = "✅" if spec.arrhythmia_type in TEMPLATES else "⬜"
                print(f"   {status} {spec.name}")
        return 0
    
    if args.all:
        templates = generate_all_templates()
        print(f"✅ Generated {len(templates)} templates")
    elif args.phase:
        templates = generate_templates_for_phase(args.phase)
        print(f"✅ Generated {len(templates)} templates for phase {args.phase}")
    else:
        parser.print_help()
        return 1
    
    # Generate Python code
    code = generate_python_code(templates)
    
    if args.output:
        Path(args.output).write_text(code)
        print(f"💾 Saved to {args.output}")
    else:
        print("\n" + "=" * 60)
        print(code)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
