# Guía Pedagógica de Simulación Clínica: Prebriefing, Briefing y Debriefing — Cardiac ECG Simulator

- **Proyecto:** `lankamar/cardiac-ecg-simulator`
- **Autor:** Lic. Marcelo Omar Lancry Kamycki (`ORCID: 0009-0008-8196-6291`)
- **Filiación:** Hospital de Clínicas «José de San Martín», Universidad de Buenos Aires (UBA) · Centro de Innovación en Tecnología y Pedagogía (CITEP–UBA)
- **Estándares de Referencia:** INACSL Standards Committee et al. (2021a, 2021b); Eppich & Cheng (2015); Rudolph et al. (2006).

---

## 1. Prebriefing — Fase de Preparación (Previo al Escenario)
Conforme al estándar *Prebriefing: Preparation and Briefing* (INACSL Standards Committee et al., 2021a), antes de iniciar la sesión práctica con el simulador se entrega al participante:
1. **Objetivos de aprendizaje explícitos:** reconocimiento sistemático de frecuencia, ritmo, onda P, intervalo PR, complejo QRS y segmento ST en 12 derivaciones.
2. **Material de lectura previa:** guía de las 54 arritmias (`docs/research/arrhythmias-54-types.md`) y criterios de electrofisiología (`docs/research/electrophysiology-models.md`).
3. **Verificación de conocimientos basales:** anatomía del sistema de conducción y lectura básica de ritmo sinusal normal.

## 2. Prebriefing — Fase de Briefing (Antes de Encender el Escenario)
Inmediatamente antes de proyectar los trazados:
1. **Seguridad psicológica y contrato de ficción:** Se explicita que la simulación es un espacio formativo seguro orientado al aprendizaje y a la seguridad del paciente, no punitivo (Rudolph et al., 2006).
2. **Orientación tecnológica al simulador:** Se explica qué capa fisiológica está activa (`SimpleLayer`, `IntermediateLayer` o `RealisticLayer`), la velocidad de papel estándar (`25 mm/s`), la escala de amplitud (`10 mm/mV`) y las limitaciones de fidelidad del entorno *in-silico*.
3. **Asignación de roles:** Líder clínico, lector de trazado en 12 derivaciones y registrador de conducta terapéutica.

## 3. Ejecución del Escenario Simulado
El facilitador ejecuta la secuencia clínica (p. ej., evolución desde ritmo sinusal normal hacia fibrilación auricular rápida o taquicardia ventricular monomórfica) y observa la toma de decisiones del equipo sin interrumpir el flujo diagnóstico.

## 4. Debriefing Estructurado (PEARLS + Good Judgment)
Al finalizar, se desarrolla el debriefing siguiendo el estándar *The Debriefing Process* (INACSL Standards Committee et al., 2021b), las 4 fases de **PEARLS** (Eppich & Cheng, 2015) y la indagación con buen juicio (Rudolph et al., 2006):
1. **Reacción:** *«¿Cómo se sintieron al identificar la transición del trazado?»*
2. **Descripción:** Síntesis objetiva del caso clínico simulado y de la arritmia presentada.
3. **Análisis (*Advocacy-Inquiry* + enseñanza directa):** Explorar qué señal morfológica guió la decisión del estudiante y corregir criterios electrocardiográficos (p. ej., presencia o ausencia de onda P, anchura del QRS).
4. **Resumen / Aplicación:** 2 aprendizajes clave transferibles a la práctica asistencial real.

---

## Referencias (Norma APA 7.ª Edición)
- Eppich, W., & Cheng, A. (2015). Promoting Excellence and Reflective Learning in Simulation (PEARLS): Development and rationale for a blended approach to health care simulation debriefing. *Simulation in Healthcare*, *10*(2), 106–115. https://doi.org/10.1097/SIH.0000000000000072
- INACSL Standards Committee, McDermott, D. S., Ludlow, J., Horsley, E., & Meakim, C. (2021a). Healthcare Simulation Standards of Best Practice™ Prebriefing: Preparation and Briefing. *Clinical Simulation in Nursing*, *58*, 9–13. https://doi.org/10.1016/j.ecns.2021.08.008
- INACSL Standards Committee, Decker, S., Alinier, G., Crawford, S. B., Gordon, R. M., Jenkins, D., & Wilson, C. (2021b). Healthcare Simulation Standards of Best Practice™ The Debriefing Process. *Clinical Simulation in Nursing*, *58*, 27–32. https://doi.org/10.1016/j.ecns.2021.08.011
- Rudolph, J. W., Simon, R., Dufresne, R. L., & Raemer, D. B. (2006). There’s no such thing as “nonjudgmental” debriefing: A theory and method for debriefing with good judgment. *Simulation in Healthcare*, *1*(1), 49–55. https://doi.org/10.1097/01266021-200600110-00006
