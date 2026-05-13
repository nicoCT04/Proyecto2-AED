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

## Resultados principales

- DP escala linealmente con `n·W` (R² ≈ 0.9997 para regresión lineal forzada),
  lo que confirma empíricamente la complejidad teórica O(n·W).
- Greedy permanece prácticamente plano y es entre 10³ y 10⁴ veces más rápido
  que DP en las instancias mayores.
- Greedy NO es óptimo en general: contraejemplo C = {1, 7, 24, 42}, W = 48,
  donde greedy entrega 7 monedas frente a 2 monedas óptimas.