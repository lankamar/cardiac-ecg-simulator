"""
Cardiac ECG Simulator - Command Line Interface.

Usage:
    python -m src.cli generate --arrhythmia afib --duration 10 --output ecg.png
    python -m src.cli list
    python -m src.cli info --arrhythmia vt_mono
"""

import argparse
import sys
from typing import Optional


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog='cardiac-sim',
        description='🫀 Cardiac ECG Simulator - Generate realistic ECG signals'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate ECG signal')
    gen_parser.add_argument(
        '-a', '--arrhythmia',
        type=str,
        default='normal_sinus_rhythm',
        help='Arrhythmia type (e.g., atrial_fibrillation, vt_mono)'
    )
    gen_parser.add_argument(
        '-d', '--duration',
        type=float,
        default=10.0,
        help='Duration in seconds (default: 10)'
    )
    gen_parser.add_argument(
        '-l', '--leads',
        type=str,
        nargs='+',
        default=['II'],
        help='Leads to generate (default: II)'
    )
    gen_parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file path (PNG/PDF/SVG). If not specified, displays plot.'
    )
    gen_parser.add_argument(
        '-n', '--noise',
        type=float,
        default=0.02,
        help='Noise level 0-1 (default: 0.02)'
    )
    gen_parser.add_argument(
        '--layer',
        type=str,
        choices=['simple', 'intermediate', 'realistic'],
        default='simple',
        help='Simulation layer (default: simple)'
    )
    
    # List command
    list_parser = subparsers.add_parser('list', help='List supported arrhythmias')
    list_parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed info for each arrhythmia'
    )
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Get arrhythmia information')
    info_parser.add_argument(
        '-a', '--arrhythmia',
        type=str,
        required=True,
        help='Arrhythmia type to get info about'
    )
    
    # Stats command
    subparsers.add_parser('stats', help='Show template coverage statistics')
    
    return parser


def cmd_generate(args) -> int:
    """Handle generate command."""
    from src.core.simulator import CardiacSimulator
    from src.arrhythmias.types import ArrhythmiaType
    
    print(f"🫀 Generating {args.arrhythmia} ECG...")
    print(f"   Duration: {args.duration}s")
    print(f"   Leads: {', '.join(args.leads)}")
    print(f"   Layer: {args.layer}")
    
    # Find arrhythmia type
    arrhythmia = None
    for arr in ArrhythmiaType:
        if arr.value == args.arrhythmia or arr.name.lower() == args.arrhythmia.lower():
            arrhythmia = arr
            break
    
    if arrhythmia is None:
        # Try partial match
        for arr in ArrhythmiaType:
            if args.arrhythmia.lower() in arr.value.lower():
                arrhythmia = arr
                break
    
    if arrhythmia is None:
        print(f"❌ Unknown arrhythmia: {args.arrhythmia}")
        print("   Use 'cardiac-sim list' to see available arrhythmias")
        return 1
    
    # Create simulator
    sim = CardiacSimulator(layer=args.layer)
    
    # Generate ECG
    ecg = sim.generate(
        arrhythmia=arrhythmia,
        duration_seconds=args.duration,
        leads=args.leads,
        noise_level=args.noise
    )
    
    print(f"   Generated {ecg.num_samples} samples")
    
    # Save or display
    if args.output:
        ecg.save(args.output)
        print(f"✅ Saved to {args.output}")
    else:
        print("   Displaying plot...")
        import matplotlib.pyplot as plt
        ecg.plot()
        plt.show()
    
    return 0


def cmd_list(args) -> int:
    """Handle list command."""
    from src.arrhythmias.types import ArrhythmiaType
    from src.data.arrhythmia_templates import TEMPLATES
    
    print("🫀 Supported Arrhythmias")
    print("=" * 60)
    
    # Group by category
    categories = {
        'supraventricular': [],
        'ventricular': [],
        'special': [],
        'normal': []
    }
    
    for arr in ArrhythmiaType:
        if 'SUPRA' in arr.name:
            categories['supraventricular'].append(arr)
        elif 'VENT' in arr.name:
            categories['ventricular'].append(arr)
        elif 'SPECIAL' in arr.name:
            categories['special'].append(arr)
        else:
            categories['normal'].append(arr)
    
    for cat_name, arrs in categories.items():
        if not arrs:
            continue
        print(f"\n📁 {cat_name.upper()} ({len(arrs)})")
        for arr in arrs:
            implemented = "✅" if arr in TEMPLATES else "⬜"
            if args.verbose:
                print(f"   {implemented} {arr.value}")
                print(f"      Enum: {arr.name}")
            else:
                print(f"   {implemented} {arr.value}")
    
    # Stats
    print(f"\n📊 Coverage: {len(TEMPLATES)}/{len(ArrhythmiaType)} " 
          f"({len(TEMPLATES)/len(ArrhythmiaType)*100:.0f}%)")
    
    return 0


def cmd_info(args) -> int:
    """Handle info command."""
    from src.arrhythmias.types import ArrhythmiaType
    from src.arrhythmias.config import get_arrhythmia_config
    from src.data.arrhythmia_templates import TEMPLATES
    
    # Find arrhythmia
    arrhythmia = None
    for arr in ArrhythmiaType:
        if args.arrhythmia.lower() in arr.value.lower():
            arrhythmia = arr
            break
    
    if arrhythmia is None:
        print(f"❌ Unknown arrhythmia: {args.arrhythmia}")
        return 1
    
    config = get_arrhythmia_config(arrhythmia)
    has_template = arrhythmia in TEMPLATES
    
    print(f"🫀 {config.name}")
    print("=" * 60)
    print(f"   Type: {arrhythmia.value}")
    print(f"   Enum: {arrhythmia.name}")
    print(f"   Template: {'✅ Implemented' if has_template else '⬜ Not implemented'}")
    print()
    print("📊 Parameters:")
    print(f"   Rate: {config.rate_range[0]}-{config.rate_range[1]} bpm")
    print(f"   Regularity: {config.rate_regularity}")
    print(f"   QRS Duration: {config.qrs_duration} ms")
    print(f"   Mechanism: {config.mechanism}")
    print(f"   Origin: {config.origin}")
    print()
    print("⚠️ Clinical:")
    print(f"   Life-threatening: {'🔴 YES' if config.is_life_threatening else '🟢 No'}")
    print(f"   Urgency: {config.urgency.upper()}")
    
    if hasattr(config, 'special_features') and config.special_features:
        print()
        print("📝 Special Features:")
        for feat in config.special_features:
            print(f"   • {feat}")
    
    return 0


def cmd_stats(args) -> int:
    """Handle stats command."""
    from src.data.arrhythmia_templates import get_template_stats
    
    stats = get_template_stats()
    
    print("🫀 Template Coverage Statistics")
    print("=" * 60)
    print(f"   Implemented: {stats['implemented']}")
    print(f"   Total: {stats['total']}")
    print(f"   Coverage: {stats['coverage']}")
    print()
    print("✅ Implemented arrhythmias:")
    for name in stats['arrhythmias']:
        print(f"   • {name}")
    
    return 0


def main(argv: Optional[list] = None) -> int:
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)
    
    if args.command is None:
        parser.print_help()
        return 0
    
    if args.command == 'generate':
        return cmd_generate(args)
    elif args.command == 'list':
        return cmd_list(args)
    elif args.command == 'info':
        return cmd_info(args)
    elif args.command == 'stats':
        return cmd_stats(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
