# Product Requirements Document (PRD)
# Cardiac ECG Simulator

**Version:** 0.1.0  
**Author:** Lankamar  
**Date:** Diciembre 2024

---

## 1. Resumen Ejecutivo

### Visión
Crear un simulador profesional de ECG que genere señales electrocardiográficas realistas para las 54 arritmias cardíacas principales, utilizando una arquitectura de 3 capas que permite balance entre rendimiento y precisión.

### Objetivos
- Simular 54 tipos de arritmias cardíacas con precisión científica
- Ofrecer 3 niveles de simulación (Simple → Intermedio → Realista)
- Generar ECG de 12 derivaciones estándar
- Proporcionar API Python fácil de usar
- Documentar fisiopatología y características ECG de cada arritmia

---

## 2. Público Objetivo

| Segmento | Uso Principal | Requisitos |
|----------|---------------|------------|
| Estudiantes de Medicina | Aprendizaje de arritmias | Simplicidad, ejemplos claros |
| Residentes de Cardiología | Entrenamiento diagnóstico | Realismo, casos variados |
| Investigadores | Validación de algoritmos | Precisión científica, parámetros ajustables |
| Desarrolladores ML | Datos de entrenamiento | API programática, generación masiva |

---

## 3. Características Principales

### 3.1 Arquitectura de 3 Capas

#### Capa Simple (v1.0)
- **Latencia:** < 1ms
- **Método:** Tablas de búsqueda, plantillas predefinidas
- **Uso:** Tiempo real, demostraciones, entrenamiento básico

#### Capa Intermedia (v2.0)
- **Latencia:** 10-100ms
- **Método:** Modelos paramétricos, ecuaciones gaussianas
- **Uso:** Entrenamiento clínico, simulaciones interactivas

#### Capa Realista (v3.0)
- **Latencia:** Segundos a minutos
- **Método:** Hodgkin-Huxley, propagación en tejido
- **Uso:** Investigación, validación científica

### 3.2 Arritmias Soportadas

| Categoría | Cantidad | Ejemplos |
|-----------|----------|----------|
| Supraventriculares | 30 | FA, Flutter, AVNRT, WPW |
| Ventriculares | 16 | TV, FV, Torsades, PVCs |
| Fenómenos Especiales | 8 | Parasistolia, R-on-T |
| **Total** | **54** | |

### 3.3 Derivaciones ECG

12 derivaciones estándar:
- Derivaciones de extremidades: I, II, III, aVR, aVL, aVF
- Derivaciones precordiales: V1-V6

---

## 4. Requisitos Funcionales

### RF-001: Generación de ECG
- [x] Generar señal ECG para cualquiera de las 54 arritmias
- [x] Duración configurable (1s - 1h)
- [x] Frecuencia de muestreo configurable (250-2000 Hz)

### RF-002: Configuración de Arritmias
- [x] Parámetros ajustables por arritmia (FC, intervalos)
- [x] Variabilidad de frecuencia cardíaca (HRV)
- [x] Nivel de ruido configurable

### RF-003: Cambio Dinámico de Capas
- [x] Cambiar de capa en tiempo de ejecución
- [x] Preservar estado entre cambios
- [x] Transición suave sin discontinuidades

### RF-004: Visualización
- [x] Ploteo estilo papel ECG
- [x] Exportación a PNG, PDF, SVG
- [x] Múltiples derivaciones simultáneas

### RF-005: Exportación de Datos
- [x] Formato numpy array
- [x] Serialización JSON
- [x] Metadatos de arritmia incluidos

---

## 5. Requisitos No Funcionales

### RNF-001: Rendimiento
- Capa Simple: < 1ms para 10s de ECG
- Capa Intermedia: < 100ms para 10s de ECG
- Capa Realista: < 60s para 10s de ECG

### RNF-002: Compatibilidad
- Python 3.9+
- Dependencias mínimas (numpy, scipy, matplotlib)
- Sin dependencias de sistema específicas

### RNF-003: Precisión
- Intervalos ECG dentro de ±5% de valores clínicos
- Morfologías distinguibles por expertos
- Validación contra bases de datos estándar (PhysioNet)

---

## 6. Roadmap

### Fase 1: v0.1.0 (Actual)
- [x] Estructura del proyecto
- [x] Enumeración 54 arritmias
- [x] Capa Simple funcional
- [x] Tests básicos

### Fase 2: v0.2.0 (Q1 2025)
- [ ] Capa Intermedia completa
- [ ] 12 derivaciones completas
- [ ] CLI básico

### Fase 3: v0.3.0 (Q2 2025)
- [ ] Capa Realista (Hodgkin-Huxley)
- [ ] Validación con datos reales
- [ ] Documentación API

### Fase 4: v1.0.0 (Q3 2025)
- [ ] UI Web básica
- [ ] Generación masiva de datasets
- [ ] Publicación PyPI

---

## 7. Métricas de Éxito

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| Cobertura de arritmias | 54/54 | Tipos implementados |
| Precisión intervalos | ±5% | Comparación con PhysioNet |
| Latencia Capa Simple | < 1ms | Benchmark |
| Cobertura de tests | > 80% | pytest-cov |
| Satisfacción usuarios | > 4/5 | Encuestas |

---

## 8. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Complejidad Hodgkin-Huxley | Alta | Alto | Implementación incremental |
| Validación científica | Media | Alto | Colaboración con cardiólogos |
| Performance insuficiente | Media | Medio | Optimización con NumPy/Cython |

---

*Documento PRD - Cardiac ECG Simulator v0.1.0*
