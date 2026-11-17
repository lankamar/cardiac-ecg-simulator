# Matriz Teleológica «Con Propósito» — Cardiac ECG Simulator

- **Proyecto:** `lankamar/cardiac-ecg-simulator`
- **Autor:** Lic. Marcelo Omar Lancry Kamycki (`ORCID: 0009-0008-8196-6291`)
- **Filiación:** Hospital de Clínicas «José de San Martín», Universidad de Buenos Aires (UBA) · Centro de Innovación en Tecnología y Pedagogía (CITEP–UBA)
- **DOI Zenodo:** `10.5281/zenodo.24326144` (Todas las versiones) · `10.5281/zenodo.24326145` (Versión 2.0.0)

---

## 1. Dolores que cubre (Planteamiento del Problema)
1. **Baja retención diagnóstica con enseñanza exclusivamente expositiva:** Las clases magistrales con tiras estáticas generan menor retención que la simulación activa (Ardekani et al., 2023; Tubaishat & Tawalbeh, 2015; Viljoen et al., 2020).
2. **Simuladores técnicos sin marco pedagógico INACSL:** Muchos softwares de ECG carecen de guías formales de *Prebriefing*, *Briefing* y *Debriefing* (INACSL Standards Committee et al., 2021a, 2021b).
3. **Brecha entre simplicidad en tiempo real y rigor electrofisiológico:** Se requiere alternar entre latencia sub-milisegundo para docencia y ecuaciones iónicas de Hodgkin y Huxley (1952) para investigación.

## 2. Justificación, Propósito, Misión y Visión
- **Justificación:** El entrenamiento seguro en reconocimiento de arritmias impacta directamente en la seguridad del paciente sin exponer a pacientes reales durante la curva de aprendizaje.
- **Propósito:** Unificar en un artefacto abierto bajo DSRM (Peffers et al., 2007) la síntesis de 54 arritmias en 12 derivaciones con la pedagogía de simulación basada en evidencia.
- **Misión:** Proveer un motor Python en 3 capas (`SimpleLayer`, `IntermediateLayer`, `RealisticLayer`) acompañado de guías de *Prebriefing*, *Briefing* y *Debriefing* (PEARLS / Good Judgment).
- **Visión:** Consolidar una plataforma abierta de simulación electrocardiográfica para formación en enfermería crítica y medicina universitaria.

## 3. Alcance y Límites
- **Incluye:** Motor Python en 3 capas, 54 arritmias + ritmo sinusal, 12 derivaciones estándar, guía pedagógica INACSL (`docs/SIMULACION_PREBRIEFING_DEBRIEFING.md`) y paper APA 7 (`paper/Kamycki_2026_Cardiac_ECG_Simulator.pdf`).
- **Excluye:** Ensayos clínicos con pacientes reales o procesamiento de historias clínicas (cumplimiento estricto Ley N.° 25.326).
