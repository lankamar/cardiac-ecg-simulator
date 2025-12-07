# 🫀 Cardiac ECG Simulator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](.github/workflows/tests.yml)

**Simulador profesional de electrocardiogramas con 54 arritmias cardíacas y arquitectura de 3 capas superpuestas.**

## 🎯 Características

- **54 Arritmias Documentadas**: Supraventriculares, ventriculares, de conducción y fenómenos especiales
- **3 Capas de Simulación**:
  - 🟢 **Simple Layer**: Lookup tables, <1ms latencia (entrenamiento)
  - 🟡 **Intermediate Layer**: Modelos parametrizados, 10-100ms (clínica)
  - 🔴 **Realistic Layer**: Hodgkin-Huxley completo (investigación)
- **12 Derivaciones ECG**: Standard limb + precordial leads
- **Fundamentado en Ciencia**: Basado en Hodgkin-Huxley 1952, Luo & Rudy 1991, ten Tusscher 2004

## 🚀 Instalación

```bash
# Clonar repositorio
git clone https://github.com/lankamar/cardiac-ecg-simulator.git
cd cardiac-ecg-simulator

# Instalar dependencias
pip install -e .

# Ejecutar tests
pytest tests/ -v
```

## 📖 Uso Rápido

```python
from src.core.simulator import CardiacSimulator
from src.arrhythmias import ArrhythmiaType

# Crear simulador
sim = CardiacSimulator(layer='simple')

# Generar ECG de fibrilación auricular
ecg = sim.generate(
    arrhythmia=ArrhythmiaType.ATRIAL_FIBRILLATION,
    duration_seconds=10,
    leads=['II', 'V1', 'V5']
)

# Plotear resultado
ecg.plot()
ecg.save('afib_example.png')
```

## 🏗️ Arquitectura de 3 Capas

```
┌─────────────────────────────────────────────────────────┐
│                    REALISTIC LAYER                      │
│   Hodgkin-Huxley • Bidomain • 3D Tissue Propagation    │
│                  (Segundos de cómputo)                  │
├─────────────────────────────────────────────────────────┤
│                  INTERMEDIATE LAYER                     │
│   Parametric Models • Pre-computed Templates           │
│                  (10-100ms latencia)                    │
├─────────────────────────────────────────────────────────┤
│                    SIMPLE LAYER                         │
│   Lookup Tables • Direct Morphology • Real-time        │
│                  (<1ms latencia)                        │
└─────────────────────────────────────────────────────────┘
```

## 📊 Arritmias Soportadas

| Categoría | Cantidad | Ejemplos |
|-----------|----------|----------|
| Supraventriculares Bradicardia | 6 | Bradicardia sinusal, Bloqueos AV |
| Supraventriculares Taquicardia | 14 | FA, Flutter, AVNRT, WPW |
| Ventriculares | 16 | TV, FV, Torsades de Pointes |
| Fenómenos Especiales | 8 | Parasistolia, R-on-T |
| **Total** | **54** | |

## 📁 Estructura del Proyecto

```
cardiac-ecg-simulator/
├── src/
│   ├── core/           # Núcleo del simulador
│   ├── layers/         # Capas: simple, intermediate, realistic
│   ├── arrhythmias/    # 54 tipos de arritmias
│   ├── ecg/            # Generación de ECG 12-lead
│   ├── models/         # Modelos matemáticos (HH, LuoRudy)
│   └── utils/          # Utilidades
├── tests/              # Tests unitarios y de integración
├── docs/
│   ├── research/       # Investigación científica
│   ├── specifications/ # Especificaciones técnicas
│   └── development/    # Documentación de desarrollo
├── examples/           # Scripts de ejemplo
└── .github/workflows/  # CI/CD
```

## 📚 Documentación

- [PRD - Product Requirements](docs/PRD.md)
- [Arquitectura](docs/ARCHITECTURE.md)
- [54 Arritmias Completas](docs/research/arrhythmias-54-types.md)
- [Modelos Electrofisiológicos](docs/research/electrophysiology-models.md)
- [Guía de Algoritmo](docs/specifications/algorithm-guide.md)

## 🔬 Referencias Científicas

- Hodgkin & Huxley (1952) - Ecuaciones fundamentales de potencial de acción
- Noble (1962) - Primer modelo de célula cardíaca
- Luo & Rudy (1991, 1994) - Modelos clásicos ventriculares
- ten Tusscher et al. (2004) - Modelo humano completo
- O'Hara & Rudy (2011) - Modelo humano de última generación
- ESC/ACC Guidelines - Nomenclatura y clasificación estándar

## 🤝 Contribuir

1. Fork este repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-arritmia`)
3. Commit tus cambios (`git commit -am 'Agregar nueva arritmia XYZ'`)
4. Push a la rama (`git push origin feature/nueva-arritmia`)
5. Crea un Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Lankamar** - [GitHub](https://github.com/lankamar)

---

⭐ Si este proyecto te es útil, considera darle una estrella!
