"""
Example: Basic ECG generation with the simulator.
"""

# Add parent directory to path for imports
import sys
sys.path.insert(0, '..')

from src.core.simulator import CardiacSimulator
from src.arrhythmias import ArrhythmiaType


def main():
    """Demonstrate basic ECG generation."""
    
    print("=" * 60)
    print("Cardiac ECG Simulator - Basic Example")
    print("=" * 60)
    
    # Create simulator with simple layer (fastest)
    print("\n1. Creating simulator with Simple Layer...")
    sim = CardiacSimulator(layer='simple')
    
    # List some supported arrhythmias
    print("\n2. Some supported arrhythmias:")
    examples = [
        ArrhythmiaType.NORMAL_SINUS,
        ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
        ArrhythmiaType.VENT_VT_MONO,
        ArrhythmiaType.VENT_VF_COARSE,
    ]
    for arr in examples:
        print(f"   - {arr.value}")
    
    # Generate normal sinus rhythm
    print("\n3. Generating Normal Sinus Rhythm (10 seconds)...")
    ecg_normal = sim.generate(
        arrhythmia=ArrhythmiaType.NORMAL_SINUS,
        duration_seconds=10,
        leads=['II', 'V1'],
        noise_level=0.02
    )
    
    print(f"   - Samples generated: {ecg_normal.num_samples}")
    print(f"   - Leads: {ecg_normal.leads}")
    print(f"   - Duration: {ecg_normal.duration} seconds")
    
    # Generate atrial fibrillation
    print("\n4. Generating Atrial Fibrillation...")
    ecg_afib = sim.generate(
        arrhythmia=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
        duration_seconds=10,
        leads=['II', 'V1']
    )
    
    # Get arrhythmia information
    print("\n5. Arrhythmia information:")
    info = sim.get_arrhythmia_info(ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION)
    print(f"   - Name: {info['name']}")
    print(f"   - Rate range: {info['rate_range']} bpm")
    print(f"   - Mechanism: {info['mechanism']}")
    print(f"   - Regularity: {info['rate_regularity']}")
    
    # Switch to intermediate layer for better accuracy
    print("\n6. Switching to Intermediate Layer...")
    sim.switch_layer('intermediate')
    print(f"   - Current layer: {sim.current_layer}")
    
    # Generate again with new layer
    ecg_intermediate = sim.generate(
        arrhythmia=ArrhythmiaType.NORMAL_SINUS,
        duration_seconds=5,
        leads=['II']
    )
    
    # Save plot (if matplotlib is available)
    try:
        print("\n7. Saving ECG plot...")
        ecg_normal.save('normal_sinus_example.png')
        print("   - Saved to: normal_sinus_example.png")
    except Exception as e:
        print(f"   - Could not save plot: {e}")
    
    # Convert to numpy for further processing
    print("\n8. Converting to numpy array...")
    data = ecg_normal.to_numpy()
    print(f"   - Shape: {data.shape}")
    
    # Count total arrhythmias
    print("\n9. Arrhythmia statistics:")
    counts = ArrhythmiaType.count()
    print(f"   - Supraventricular: {counts['supraventricular']}")
    print(f"   - Ventricular: {counts['ventricular']}")
    print(f"   - Special phenomena: {counts['special']}")
    print(f"   - TOTAL: {counts['total']}")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
