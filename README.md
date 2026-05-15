# Proyecto 2 - Coin Change Problem

**Universidad del Valle de Guatemala**
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Docente: Tomás Gálvez P.

## Integrantes

- **Nicolás Concuá** - Carné No. 23197
- **Esteban Cárcamo** - Carné No. 23016
- **Diego López** - Carné No. 23747

## Problema elegido

**Coin Change (Problema del Cambio de Monedas)**

Dado un conjunto de denominaciones C = {c1, ..., cn} y un monto W, encontrar la
cantidad mínima de monedas que sumen exactamente W. Se asume disponibilidad
ilimitada de cada denominación y existencia de la moneda 1.

Se abordan **dos enfoques** sobre el mismo problema:

1. **Solución exacta con Programación Dinámica**: tabla DP bottom-up de tamaño
   `n × W`. Complejidad **O(n·W)** - pseudo-polinomial (superpolinomial respecto
   al tamaño de entrada en bits).
2. **Solución Greedy**: heurística de selección por mayor denominación primero.
   Complejidad **O(n log n)**. Solo es óptima en sistemas de monedas canónicos.

## Estructura del repositorio

```
.
├── src/
│   ├── coin_change_dp.py         # Solución por Programación Dinámica
│   ├── coin_change_greedy.py     # Heurística Greedy
│   └── benchmark.py              # Mediciones, gráficas, regresión polinomial
├── results/
│   ├── tiempos.csv               # Datos crudos del benchmark
│   └── tiempos_dispersion.png    # Diagrama de dispersión + regresiones
├── docs/
│   └── Informe_Proyecto2_CoinChange.docx
├── commits_por_integrante.txt    # Plan de commits por persona
└── README.md
```

## Cómo ejecutar

Requisitos: Python 3.10+, NumPy y Matplotlib.

```bash
# Demo rápida de cada algoritmo
python src/coin_change_dp.py
python src/coin_change_greedy.py

# Benchmark completo: genera CSV y gráfica
python src/benchmark.py
```

## Diferenciador respecto al examen parcial

Este proyecto NO resuelve el problema de coin change "estándar" con un sistema
de monedas canónico fijo (como el visto en el examen parcial). El enfoque de
este proyecto es deliberadamente **el caso general**:

1. **Denominaciones arbitrarias**: los sistemas analizados son no canónicos en
   su mayoría, generados pseudo-aleatoriamente con denominaciones en rangos
   amplios. El proyecto contrasta sistemáticamente el comportamiento de DP y
   greedy en estos sistemas.

2. **Análisis de la greedy-choice property**: se demuestra formalmente y se
   exhibe empíricamente que la propiedad NO se cumple en general, con
   contraejemplos cuantificados (ratio greedy/óptimo hasta 3.5× en el caso
   `C={1,7,24,42}, W=48`).

3. **Verificador de canonicidad** (`src/canonicity_check.py`): implementación
   del test de Pearson (2005) que decide en tiempo polinomial si un sistema
   de monedas dado es canónico, dato que el examen no contempla.

4. **Análisis adversarial** (`src/adversarial_cases.py`): generación
   sistemática de sistemas donde greedy falla, con métrica del ratio de
   aproximación greedy/óptimo.

5. **Naturaleza pseudo-polinomial del DP**: el informe discute por qué O(n·W)
   es exponencial en el tamaño de la entrada en bits (W codificado en log₂ W
   bits), distinguiendo polinomialidad numérica de polinomialidad real.

En síntesis: el examen pregunta "resolver coin change"; este proyecto pregunta
"**¿cuándo greedy es óptimo y cuándo falla, y qué tan mal puede fallar?**".

## Resultados principales

- DP escala linealmente con `n·W` (R² ≈ 0.9997 para regresión lineal forzada),
  lo que confirma empíricamente la complejidad teórica O(n·W).
- Greedy permanece prácticamente plano y es entre 10³ y 10⁴ veces más rápido
  que DP en las instancias mayores.
- Greedy NO es óptimo en general: contraejemplo C = {1, 7, 24, 42}, W = 48,
  donde greedy entrega 7 monedas frente a 2 monedas óptimas.