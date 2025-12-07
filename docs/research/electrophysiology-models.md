# 🔬 Modelos Electrofisiológicos

## Fundamentos Matemáticos para Simulación de ECG

---

## 1. Modelo de Hodgkin-Huxley (1952)

### Ecuación Fundamental

La corriente transmembrana se describe como:

```
I_m = C_m * (dV/dt) + I_ion
```

Donde:
- `C_m`: Capacitancia de membrana (1 µF/cm²)
- `V`: Potencial de membrana (mV)
- `I_ion`: Suma de corrientes iónicas

### Corrientes Iónicas Principales

```
I_Na = g_Na * m³ * h * (V - E_Na)   # Sodio
I_K  = g_K  * n⁴ * (V - E_K)        # Potasio
I_L  = g_L  * (V - E_L)             # Fuga
```

### Variables de Compuerta

Las variables de compuerta (m, h, n) siguen:

```
dx/dt = α_x(V) * (1 - x) - β_x(V) * x
```

Donde `α` y `β` dependen del voltaje:

```python
α_m = 0.1 * (V + 40) / (1 - exp(-(V + 40) / 10))
β_m = 4 * exp(-(V + 65) / 18)

α_h = 0.07 * exp(-(V + 65) / 20)
β_h = 1 / (1 + exp(-(V + 35) / 10))

α_n = 0.01 * (V + 55) / (1 - exp(-(V + 55) / 10))
β_n = 0.125 * exp(-(V + 65) / 80)
```

---

## 2. Modelos de Célula Cardíaca

### 2.1 Modelo de Noble (1962)
Primer modelo de célula cardíaca, adaptación de H-H con:
- Corriente de potasio rectificadora
- Corriente lenta de entrada

### 2.2 Modelo Luo-Rudy I (1991)
- 8 variables de estado
- Corrientes: I_Na, I_si, I_K, I_K1, I_Kp, I_b

### 2.3 Modelo ten Tusscher (2004)
Modelo humano con:
- 19 variables de estado
- Corrientes de Ca²⁺ sarcoplasmático
- Dinámica de calcio detallada

### 2.4 Modelo O'Hara-Rudy (2011)
Modelo humano de última generación:
- 41 variables de estado
- Validado con datos humanos
- Usado en investigación farmacológica

---

## 3. Propagación en Tejido

### Ecuación Monodomain (Simplificada)

```
∇ · (σ ∇V) = β * (C_m * ∂V/∂t + I_ion)
```

Donde:
- `σ`: Tensor de conductividad
- `β`: Relación superficie-volumen

### Ecuación Bidomain (Realista)

```
∇ · (σ_i ∇V_i) = β * I_m
∇ · (σ_e ∇V_e) = -β * I_m
V = V_i - V_e
```

### Anisotropía

La conducción es más rápida paralela a las fibras:
- Longitudinal: ~0.6 m/s
- Transversal: ~0.2 m/s

---

## 4. Problema Directo (Forward Problem)

### Cálculo del ECG de Superficie

El potencial de superficie se calcula como:

```
Φ(r) = ∫∫∫ (σ_i + σ_e) * D(V_m) · ∇G(r, r') dV'
```

Donde:
- `G`: Función de Green
- `D`: Operador de dipolo
- `V_m`: Potencial transmembrana

### Triángulo de Einthoven

Las derivaciones están relacionadas:

```
II = I + III
aVR = -(I + II) / 2
aVL = (I - III) / 2
aVF = (II + III) / 2
```

### Derivaciones Precordiales

Calculadas desde posiciones específicas en el tórax:
- V1: 4° espacio intercostal, borde esternal derecho
- V2: 4° espacio intercostal, borde esternal izquierdo
- V3: Entre V2 y V4
- V4: 5° espacio intercostal, línea medioclavicular
- V5: 5° espacio intercostal, línea axilar anterior
- V6: 5° espacio intercostal, línea medioaxilar

---

## 5. Implementación en Capas

### Capa Simple (Lookup Tables)

```python
def generate_beat_simple(params):
    p_wave = gaussian(params.p_duration, params.p_amplitude)
    qrs = qrs_template(params.qrs_duration)
    t_wave = gaussian(params.t_duration, params.t_amplitude)
    return concatenate(p_wave, pr_segment, qrs, st_segment, t_wave)
```

### Capa Intermedia (Paramétrica)

```python
def generate_beat_parametric(params, t):
    # Superposición de gaussianas
    p = A_p * exp(-((t - t_p)² / (2 * σ_p²)))
    r = A_r * exp(-((t - t_r)² / (2 * σ_r²)))
    # ... más componentes
    return p + q + r + s + t_wave
```

### Capa Realista (Hodgkin-Huxley)

```python
def simulate_cell(t_end, dt):
    V, m, h, n = initial_conditions()
    for t in range(0, t_end, dt):
        I_ion = I_Na(V, m, h) + I_K(V, n) + I_L(V)
        dV = (I_stim[t] - I_ion) / C_m
        V += dV * dt
        m, h, n = update_gates(V, m, h, n, dt)
    return V_trace
```

---

## 6. Herramientas de Referencia

| Software | Tipo | Uso |
|----------|------|-----|
| openCARP | Open source | Simulación cardíaca multiscala |
| CARP | Académico | Referencia científica |
| Chaste | Open source | Biología computacional |
| CARDIOSIM | Comercial | Fisiología integrada |

---

## Referencias

1. Hodgkin AL, Huxley AF (1952). J Physiol. 117(4):500-544
2. Noble D (1962). J Physiol. 160(2):317-352
3. Luo CH, Rudy Y (1991). Circ Res. 68(6):1501-1526
4. ten Tusscher KHWJ et al (2004). Am J Physiol. 286(4):H1573-H1589
5. O'Hara T, Rudy Y (2011). PLoS Comput Biol. 7(5):e1002061

---

*Documento generado para Cardiac ECG Simulator v0.1.0*
