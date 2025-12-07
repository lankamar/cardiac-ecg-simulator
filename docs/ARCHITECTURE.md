# 🏗️ Arquitectura del Sistema

## Cardiac ECG Simulator - Diagrama de Arquitectura

---

## Diagrama de Capas

```
┌──────────────────────────────────────────────────────────────────┐
│                         USUARIO / API                            │
│              CardiacSimulator.generate(arrhythmia)               │
└─────────────────────────────┬────────────────────────────────────┘
                              │
┌─────────────────────────────▼────────────────────────────────────┐
│                      CAPA DE ORQUESTACIÓN                        │
│                         (simulator.py)                           │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────────┐  │
│  │ Layer       │  │ Arrhythmia   │  │ ECG Signal             │  │
│  │ Manager     │  │ Config       │  │ Container              │  │
│  └─────────────┘  └──────────────┘  └────────────────────────┘  │
└─────────────────────────────┬────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   SIMPLE LAYER  │ │INTERMEDIATE LAYER│ │ REALISTIC LAYER │
│  (< 1ms)        │ │ (10-100ms)       │ │ (segundos)      │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • Lookup tables │ │ • Parametric    │ │ • Hodgkin-Huxley│
│ • Templates     │ │ • Gaussians     │ │ • Ionic currents│
│ • Direct morph  │ │ • Lead vectors  │ │ • Tissue prop   │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                    │
         └───────────────────┴────────────────────┘
                              │
                              ▼
         ┌────────────────────────────────────────┐
         │              ECGSignal                 │
         │  • signals: Dict[lead → np.array]     │
         │  • plot() / save() / to_numpy()       │
         └────────────────────────────────────────┘
```

---

## Estructura de Módulos

```
src/
├── __init__.py              # Package exports
├── core/
│   ├── simulator.py         # CardiacSimulator (orquestador)
│   └── ecg_signal.py        # ECGSignal (contenedor)
│
├── arrhythmias/
│   ├── types.py             # ArrhythmiaType Enum (54 tipos)
│   ├── config.py            # ArrhythmiaConfig (parámetros)
│   └── registry.py          # ARRHYTHMIA_REGISTRY (lookup)
│
├── layers/
│   ├── base.py              # BaseLayer (interface)
│   ├── simple_layer.py      # SimpleLayer (templates)
│   ├── intermediate_layer.py # IntermediateLayer (parametric)
│   └── realistic_layer.py   # RealisticLayer (H-H)
│
├── models/
│   ├── hodgkin_huxley.py    # H-H equations
│   ├── cell_models.py       # Cardiac cell models
│   └── tissue.py            # Tissue propagation
│
└── utils/
    ├── math_utils.py        # Gaussian, transforms
    └── lead_vectors.py      # Einthoven triangle
```

---

## Flujo de Datos

```
1. Usuario llama: sim.generate(ArrhythmiaType.ATRIAL_FIBRILLATION)
                           │
2. Simulator obtiene:      ▼
   config = get_arrhythmia_config(arrhythmia)
   └── rate_range, p_wave, qrs_duration, etc.
                           │
3. Layer.generate():       ▼
   signals = self._layer.generate(config, num_samples, leads)
   └── Cada layer implementa su propia lógica
                           │
4. Retorna:               ▼
   ECGSignal(signals, leads, sampling_rate, arrhythmia)
   └── Usuario puede plotear, exportar, analizar
```

---

## Cambio Dinámico de Capas

```python
# Estado preservado durante cambio
sim = CardiacSimulator(layer='simple')
ecg1 = sim.generate(...)

# Cambio a capa más precisa
sim.switch_layer('intermediate')  # Estado preservado
ecg2 = sim.generate(...)          # Continúa desde donde estaba

# Cambio a investigación
sim.switch_layer('realistic')     # Estado preservado
ecg3 = sim.generate(...)          # Máxima precisión
```

---

## Generación de 12 Derivaciones

```
            I = LA - RA
           /           \
         aVL            aVR
        /                 \
      LA ─────────────── RA
       \                 /
        \     Heart    /
         \    (dipole)/
          \   ┌───┐  /
           \  │ D │ /
            \ └───┘/
             \   /
              \ /
              LL ─── III = LL - RA
             /  \
           aVF   II = LL - LA
         
Precordiales (V1-V6): Proyecciones horizontales del dipolo
```

---

## Modelo de Capas Detallado

### Simple Layer
```
Input: ArrhythmiaConfig
  │
  ▼
┌─────────────────┐
│ Load Templates  │ ← P_normal, QRS_normal, T_normal
└────────┬────────┘
         │
  ▼──────┴──────▼
┌─────┐ ┌─────┐ ┌─────┐
│  P  │ │ QRS │ │  T  │  ← Selección por morfología
└──┬──┘ └──┬──┘ └──┬──┘
   └───────┼───────┘
           │
  ▼────────┴────────▼
┌─────────────────────┐
│ Concatenate + Noise │
└─────────────────────┘
         │
         ▼
    ECG Signal
```

### Realistic Layer
```
Input: ArrhythmiaConfig
  │
  ▼
┌─────────────────────┐
│ Hodgkin-Huxley Sim  │
│ dV/dt = (I_stim -   │
│  I_Na - I_K - I_L)  │
└────────┬────────────┘
         │
  ▼──────┴──────▼
┌─────────────────┐
│ Action Potential│
│     Train       │
└────────┬────────┘
         │
┌────────▼────────┐
│ Forward Problem │
│  AP → ECG proj  │
└────────┬────────┘
         │
         ▼
    ECG Signal
```

---

## Dependencias

```
numpy >= 1.21.0    ───► Operaciones numéricas
scipy >= 1.7.0     ───► FFT, filtros, integración
matplotlib >= 3.5  ───► Visualización ECG
```

---

*Diagrama de Arquitectura - Cardiac ECG Simulator v0.1.0*
