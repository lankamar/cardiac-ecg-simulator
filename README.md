# 🫀 Cardiac ECG Simulator

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen.svg)](.github/workflows/tests.yml)

**Simulador profesional de electrocardiogramas con 54 arritmias cardíacas y arquitectura de 3 capas superpuestas.**

---

## 📜 Historia y Origen del Proyecto

Este repositorio es la **Generación 3** — la versión científica y profesional — de un proyecto que nació de una colaboración académica y fue escalando progresivamente.

### La Evolución en 4 Generaciones

| Repo | Generación | Descripción |
|------|-----------|-------------|
| [`ECG-Simulator`](https://github.com/lankamar/ECG-Simulator) | V1 | Primer prototipo educativo — 12 derivaciones |
| [`ECG-Simulator-V0-Beta`](https://github.com/lankamar/ECG-Simulator-V0-Beta) | V0-Beta | IA + Mobile-first UX (Vercel) |
| [`ECG-Simulator2`](https://github.com/lankamar/ECG-Simulator2) | V2 | Colaboración con Lic. Cuence (autor de libro ECG) + Gemini AI |
| **`cardiac-ecg-simulator`** | **V3** ⭐ | **Motor científico Python — versión actual** |

El proyecto nació de una colaboración con el **Licenciado Cuence**, autor de un libro especializado en electrocardiografía, cuya base teórica fue digitalizada en `ECG-Simulator2`. A partir de allí se planteó la visión de escalar hacia un motor científico capaz de reproducir fielmente los modelos electrofisiológicos usados en investigación.

### Visión de Escala Futura
```
Nivel 1 → Visualización 2D de trazados ECG (12 derivaciones)   ✅ Implementado
Nivel 2 → IA explicativa e interactiva                          ✅ En ECG-Simulator2
Nivel 3 → Visualización 3D del recorrido eléctrico cardíaco     🔄 Planificado
Nivel 4 → Recreación de casos clínicos reales                   📋 Roadmap
Nivel 5 → Hipótesis diagnósticas asistidas por IA               📋 Roadmap
```

---

## 🎯 Características

- **54 Arritmias Documentadas**: Supraventriculares, ventriculares, de conducción y fenómenos especiales
- **3 Capas de Simulación**:
  - 🟢 **Simple Layer**: Lookup tables, <1ms latencia (entrenamiento)
  - 🟡 **Intermediate Layer**: Modelos parametrizados, 10-100ms (clínica)
  - 🔴 **Realistic Layer**: Hodgkin-Huxley completo (investigación)
- **12 Derivaciones ECG**: Standard limb + precordial leads
- **Fundamentado en Ciencia**: Basado en Hodgkin-Huxley 1952, Luo & Rudy 1991, ten Tusscher 2004

---

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

---

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

---

## 🏗️ Arquitectura de 3 Capas

```
┌─────────────────────────────────────────────────────────┐
│                    REALISTIC LAYER                       │
│          Hodgkin-Huxley • Bidomain • 3D Tissue           │
│                  (Segundos de cómputo)                   │
├─────────────────────────────────────────────────────────┤
│                  INTERMEDIATE LAYER                      │
│          Parametric Models • Pre-computed Templates      │
│                    (10-100ms latencia)                   │
├─────────────────────────────────────────────────────────┤
│                     SIMPLE LAYER                         │
│          Lookup Tables • Direct Morphology • Real-time   │
│                      (<1ms latencia)                     │
└─────────────────────────────────────────────────────────┘
```

---

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

---

## 📚 Documentación

- [PRD - Product Requirements](docs/PRD.md)
- [Arquitectura](docs/ARCHITECTURE.md)
- [54 Arritmias Completas](docs/research/arrhythmias-54-types.md)
- [Modelos Electrofisiológicos](docs/research/electrophysiology-models.md)
- [Guía de Algoritmo](docs/specifications/algorithm-guide.md)

---

## 🔬 Referencias Científicas

- Hodgkin & Huxley (1952) - Ecuaciones fundamentales de potencial de acción
- Noble (1962) - Primer modelo de célula cardíaca
- Luo & Rudy (1991, 1994) - Modelos clásicos ventriculares
- ten Tusscher et al. (2004) - Modelo humano completo
- O'Hara & Rudy (2011) - Modelo humano de última generación
- ESC/ACC Guidelines - Nomenclatura y clasificación estándar

---

## 🤝 Contribuir

1. Fork este repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-arritmia`)
3. Commit tus cambios (`git commit -am 'Agregar nueva arritmia XYZ'`)
4. Push a la rama (`git push origin feature/nueva-arritmia`)
5. Crea un Pull Request

---

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

---

## 👨‍💻 Autor

**Lankamar** — [GitHub](https://github.com/lankamar)

⭐ Si este proyecto te es útil, considera darle una estrella!
