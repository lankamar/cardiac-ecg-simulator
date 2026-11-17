# 🫀 Cardiac ECG Simulator
### *Arquitectura Electrofisiológica en Tres Capas y Marco Pedagógico de Simulación Clínica (Prebriefing, Briefing y Debriefing) para la Enseñanza de Arritmias*

[![Zenodo DOI (All Versions)](https://zenodo.org/badge/DOI/10.5281/zenodo.24326144.svg)](https://doi.org/10.5281/zenodo.24326144)
[![Zenodo DOI v2.0.0](https://zenodo.org/badge/DOI/10.5281/zenodo.24326145.svg)](https://doi.org/10.5281/zenodo.24326145)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0008--8196--6291-A6CE39?logo=orcid&logoColor=white)](https://orcid.org/0009-0008-8196-6291)
[![Google Scholar](https://img.shields.io/badge/Google_Scholar-ERLQOWcAAAAJ-4285F4?logo=google-scholar&logoColor=white)](https://scholar.google.com/citations?user=ERLQOWcAAAAJ&hl=es)
[![APA 7th Edition](https://img.shields.io/badge/Standard-APA_7th_Edition-blue.svg)](https://apastyle.apa.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

- **Autor:** Lic. Marcelo Omar Lancry Kamycki
- **Filiación Institucional:** Hospital de Clínicas «José de San Martín», Universidad de Buenos Aires (UBA) · Centro de Innovación en Tecnología y Pedagogía (CITEP–UBA)
- **ORCID:** [https://orcid.org/0009-0008-8196-6291](https://orcid.org/0009-0008-8196-6291)
- **Google Académico:** [https://scholar.google.com/citations?user=ERLQOWcAAAAJ&hl=es](https://scholar.google.com/citations?user=ERLQOWcAAAAJ&hl=es)
- **Sitio Institucional:** [https://lankamar.github.io/](https://lankamar.github.io/)
- **DOI Zenodo (Todas las versiones):** [https://doi.org/10.5281/zenodo.24326144](https://doi.org/10.5281/zenodo.24326144)
- **DOI Versión 2.0.0 (APA 7.ª ed. Verificada):** [https://doi.org/10.5281/zenodo.24326145](https://doi.org/10.5281/zenodo.24326145)
- **Paper Completo en PDF (Norma APA 7.ª ed.):** [paper/Kamycki_2026_Cardiac_ECG_Simulator.pdf](paper/Kamycki_2026_Cardiac_ECG_Simulator.pdf)
- **Guía de Simulación Clínica (Prebriefing, Briefing y Debriefing):** [docs/SIMULACION_PREBRIEFING_DEBRIEFING.md](docs/SIMULACION_PREBRIEFING_DEBRIEFING.md)

---

## Resumen Académico (Norma APA 7.ª Edición)

La interpretación rápida y precisa de arritmias cardíacas constituye una competencia crítica en enfermería de cuidados intensivos y medicina clínica; sin embargo, la enseñanza basada únicamente en clases magistrales y trazados estáticos presenta limitaciones documentadas en la retención del conocimiento y la transferencia diagnóstica (Ardekani et al., 2023; Tubaishat & Tawalbeh, 2015; Viljoen et al., 2020). Enmarcado en la Metodología de Investigación en Ciencia del Diseño (DSRM; Peffers et al., 2007), **Cardiac ECG Simulator** implementa un motor de simulación electrocardiográfica en Python de 12 derivaciones estándar que integra 54 arritmias cardíacas (además del ritmo sinusal normal) sobre una arquitectura superpuesta de tres capas fisiológicas: `SimpleLayer` (tablas de morfología), `IntermediateLayer` (modelos paramétricos) y `RealisticLayer` (ecuaciones iónicas adaptadas de Hodgkin & Huxley, 1952), contextualizada en la síntesis matemática de señales ECG (McSharry et al., 2003). Su uso educativo se articula explícitamente con los estándares internacionales de simulación clínica: **Prebriefing** (Preparación y Briefing; INACSL Standards Committee et al., 2021a), ejecución del escenario simulado y **Debriefing** estructurado mediante los marcos **PEARLS** (Eppich & Cheng, 2015) y *Debriefing with Good Judgment* (INACSL Standards Committee et al., 2021b; Rudolph et al., 2006).

---

## Ciclo Pedagógico de Simulación Clínica (INACSL 2021 + PEARLS)

1. **Prebriefing — Preparación:** Entrega previa de objetivos de aprendizaje, guía de las 54 arritmias (`docs/research/arrhythmias-54-types.md`) y criterios basales de lectura ECG (INACSL Standards Committee et al., 2021a).
2. **Prebriefing — Briefing:** Contrato de ficción, seguridad psicológica, orientación a las 12 derivaciones y a la capa activa (`simple`, `intermediate`, `realistic`), y asignación de roles (Rudolph et al., 2006).
3. **Escenario Simulado:** Generación y transición dinámica de trazados ECG en tiempo real.
4. **Debriefing Estructurado:** Sesión reflexiva en 4 fases (Reacción, Descripción, Análisis *Advocacy-Inquiry*, Resumen/Aplicación) bajo **PEARLS** (Eppich & Cheng, 2015) e **INACSL** (INACSL Standards Committee et al., 2021b).

Ver desarrollo completo en [docs/SIMULACION_PREBRIEFING_DEBRIEFING.md](docs/SIMULACION_PREBRIEFING_DEBRIEFING.md) y [docs/PROPOSITO.md](docs/PROPOSITO.md).

---

## Arquitectura Técnica de 3 Capas y Uso Rápido

- **54 Arritmias + Ritmo Sinusal Normal** (`55` entradas en `src/arrhythmias/types.py`) y **12 derivaciones estándar** (`I, II, III, aVR, aVL, aVF, V1–V6`).
- **Simple Layer** (`src/layers/simple_layer.py`): tablas morfológicas (`< 1 ms` de latencia).
- **Intermediate Layer** (`src/layers/intermediate_layer.py`): modelos paramétricos (`10–100 ms`).
- **Realistic Layer** (`src/layers/realistic_layer.py`): ecuaciones iónicas de Hodgkin y Huxley (1952) con compuertas `m, h, n` y canales `Na+`, `K+`, `Leak`.

```bash
git clone https://github.com/lankamar/cardiac-ecg-simulator.git
cd cardiac-ecg-simulator
pip install -e .
pytest tests/ -v
```

```python
from src.core.simulator import CardiacSimulator
from src.arrhythmias import ArrhythmiaType

sim = CardiacSimulator(layer='simple')
ecg = sim.generate(
    arrhythmia=ArrhythmiaType.SUPRA_TACHY_ATRIAL_FIBRILLATION,
    duration_seconds=10,
    leads=['II', 'V1', 'V5']
)
ecg.plot()
```

---

## Cómo citar este trabajo (Norma APA 7.ª Edición)

> Lancry Kamycki, M. O. (2026). *Cardiac ECG Simulator: Arquitectura electrofisiológica en tres capas y marco pedagógico de simulación clínica (Prebriefing, Briefing y Debriefing) para la enseñanza de arritmias* (Version 2.0.0). Zenodo. https://doi.org/10.5281/zenodo.24326145

---

## Referencias Bibliográficas (Norma APA 7.ª Edición)

- Ardekani, A., Hider, A. M., Rastegar Kazerooni, A. A., Hosseini, S. A., Roshanshad, A., Amini, M., & Kojuri, J. (2023). Surfing the clinical trials of ECG teaching to medical students: A systematic review. *Journal of Education and Health Promotion*, *12*, Article 107. https://doi.org/10.4103/jehp.jehp_780_22
- Eppich, W., & Cheng, A. (2015). Promoting Excellence and Reflective Learning in Simulation (PEARLS): Development and rationale for a blended approach to health care simulation debriefing. *Simulation in Healthcare*, *10*(2), 106–115. https://doi.org/10.1097/SIH.0000000000000072
- Hodgkin, A. L., & Huxley, A. F. (1952). A quantitative description of membrane current and its application to conduction and excitation in nerve. *The Journal of Physiology*, *117*(4), 500–544. https://doi.org/10.1113/jphysiol.1952.sp004764
- INACSL Standards Committee, McDermott, D. S., Ludlow, J., Horsley, E., & Meakim, C. (2021a). Healthcare Simulation Standards of Best Practice™ Prebriefing: Preparation and Briefing. *Clinical Simulation in Nursing*, *58*, 9–13. https://doi.org/10.1016/j.ecns.2021.08.008
- INACSL Standards Committee, Decker, S., Alinier, G., Crawford, S. B., Gordon, R. M., Jenkins, D., & Wilson, C. (2021b). Healthcare Simulation Standards of Best Practice™ The Debriefing Process. *Clinical Simulation in Nursing*, *58*, 27–32. https://doi.org/10.1016/j.ecns.2021.08.011
- McSharry, P. E., Clifford, G. D., Tarassenko, L., & Smith, L. A. (2003). A dynamical model for generating synthetic electrocardiogram signals. *IEEE Transactions on Biomedical Engineering*, *50*(3), 289–294. https://doi.org/10.1109/TBME.2003.808805
- Peffers, K., Tuunanen, T., Rothenberger, M. A., & Chatterjee, S. (2007). A design science research methodology for information systems research. *Journal of Management Information Systems*, *24*(3), 45–77. https://doi.org/10.2753/MIS0742-1222240302
- Rudolph, J. W., Simon, R., Dufresne, R. L., & Raemer, D. B. (2006). There’s no such thing as “nonjudgmental” debriefing: A theory and method for debriefing with good judgment. *Simulation in Healthcare*, *1*(1), 49–55. https://doi.org/10.1097/01266021-200600110-00006
- Tubaishat, A., & Tawalbeh, L. I. (2015). Effect of cardiac arrhythmia simulation on nursing students’ knowledge acquisition and retention. *Western Journal of Nursing Research*, *37*(9), 1160–1174. https://doi.org/10.1177/0193945914545134
- Viljoen, C. A., Millar, R. S., Manning, K., & Burch, V. C. (2020). Effectiveness of blended learning versus lectures alone on ECG analysis and interpretation by medical students. *BMC Medical Education*, *20*(1), Article 488. https://doi.org/10.1186/s12909-020-02403-y
