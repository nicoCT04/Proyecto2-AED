"""
benchmark.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Análisis Empírico)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Mide el tiempo de ejecución de las implementaciones DP y greedy del
    problema del cambio de monedas para distintos tamaños de entrada,
    genera un diagrama de dispersión y ajusta una regresión polinomial a
    cada serie de tiempos.

    Como tamaño de entrada usamos n_W = n * W, que coincide con el costo
    teórico del DP. Esto permite mostrar empíricamente que DP escala
    linealmente respecto a n*W (pseudo-polinomial), mientras que greedy es
    prácticamente constante en escala logarítmica.
"""

from __future__ import annotations
import time
import random
import csv
import os
import sys
from typing import List, Tuple


class _Tee:
    """Escribe simultáneamente en stdout y en un archivo."""

    def __init__(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self._file = open(path, "w", encoding="utf-8")
        self._stdout = sys.stdout

    def write(self, data: str) -> None:
        self._stdout.write(data)
        self._file.write(data)

    def flush(self) -> None:
        self._stdout.flush()
        self._file.flush()

    def __enter__(self) -> "_Tee":
        sys.stdout = self
        return self

    def __exit__(self, *_) -> None:
        sys.stdout = self._stdout
        self._file.close()

import numpy as np
import matplotlib
matplotlib.use("Agg")  # backend sin GUI para guardar imágenes
import matplotlib.pyplot as plt

from coin_change_dp import coin_change_dp
from coin_change_greedy import coin_change_greedy


# ----------------------------------------------------------------------------
# Generación de casos de prueba
# ----------------------------------------------------------------------------

def generar_caso(n: int, W: int, seed: int) -> List[int]:
    """Genera un sistema de monedas con n denominaciones aleatorias.

    Siempre se incluye la denominación 1 para garantizar que cualquier W
    sea representable por el DP. Las demás denominaciones se eligen
    aleatoriamente en [2, max(2, W//2)] para producir sistemas no canónicos.
    """
    rng = random.Random(seed)
    coins = {1}
    cota_sup = max(2, W // 2)
    intentos = 0
    while len(coins) < n and intentos < 50 * n:
        coins.add(rng.randint(2, cota_sup))
        intentos += 1
    # Si no se logró el tamaño n por valores repetidos, agregamos secuencialmente.
    extra = 2
    while len(coins) < n:
        coins.add(extra)
        extra += 1
    return sorted(coins)


# ----------------------------------------------------------------------------
# Utilidades de medición
# ----------------------------------------------------------------------------

def medir(funcion, coins: List[int], W: int, repeticiones: int = 3) -> float:
    """Devuelve el tiempo promedio en segundos sobre `repeticiones` corridas."""
    tiempos = []
    for _ in range(repeticiones):
        t0 = time.perf_counter()
        funcion(coins, W)
        t1 = time.perf_counter()
        tiempos.append(t1 - t0)
    return sum(tiempos) / len(tiempos)


# ----------------------------------------------------------------------------
# Experimento principal
# ----------------------------------------------------------------------------

def correr_experimento() -> Tuple[List[dict], str, str]:
    """Corre el experimento y devuelve (filas, ruta_csv, ruta_png)."""
    # Cada caso es (n, W). Diversificamos para cubrir distintas escalas.
    casos: List[Tuple[int, int]] = [
        (5,    100),
        (5,    500),
        (5,   1000),
        (8,   1000),
        (8,   2500),
        (10,  2500),
        (10,  5000),
        (12,  5000),
        (12, 10000),
        (15, 10000),
        (15, 20000),
        (20, 20000),
        (20, 40000),
        (25, 40000),
        (25, 80000),
    ]

    filas: List[dict] = []
    print(f"{'n':>4} {'W':>8} {'n*W':>10} {'DP (s)':>12} {'Greedy (s)':>12}")
    print("-" * 52)

    for i, (n, W) in enumerate(casos):
        coins = generar_caso(n, W, seed=42 + i)
        t_dp = medir(coin_change_dp, coins, W, repeticiones=3)
        t_gr = medir(coin_change_greedy, coins, W, repeticiones=3)
        fila = {
            "n": n,
            "W": W,
            "nW": n * W,
            "t_dp": t_dp,
            "t_greedy": t_gr,
            "coins": coins,
        }
        filas.append(fila)
        print(f"{n:>4} {W:>8} {n*W:>10} {t_dp:>12.6f} {t_gr:>12.6f}")

    # Carpeta de resultados
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base, "results")
    os.makedirs(out_dir, exist_ok=True)

    # CSV con los datos
    csv_path = os.path.join(out_dir, "tiempos.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "W", "n*W", "t_dp_seg", "t_greedy_seg", "coins"])
        for r in filas:
            writer.writerow([r["n"], r["W"], r["nW"], f"{r['t_dp']:.8f}",
                             f"{r['t_greedy']:.8f}", str(r["coins"])])

    # Gráfica
    png_path = os.path.join(out_dir, "tiempos_dispersion.png")
    graficar(filas, png_path)

    return filas, csv_path, png_path


# ----------------------------------------------------------------------------
# Regresión polinomial y visualización
# ----------------------------------------------------------------------------

def ajustar_polinomio(x: np.ndarray, y: np.ndarray, grados=(1, 2, 3)):
    """Ajusta polinomios de varios grados y devuelve el mejor (mayor R^2)."""
    mejor = None
    for g in grados:
        coefs = np.polyfit(x, y, g)
        y_hat = np.polyval(coefs, x)
        ss_res = np.sum((y - y_hat) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 1.0
        if mejor is None or r2 > mejor["r2"]:
            mejor = {"grado": g, "coefs": coefs, "r2": r2}
    return mejor


def formatear_polinomio(coefs: np.ndarray) -> str:
    """Devuelve una representación legible del polinomio."""
    grado = len(coefs) - 1
    partes = []
    for i, c in enumerate(coefs):
        p = grado - i
        if p == 0:
            partes.append(f"{c:.3e}")
        elif p == 1:
            partes.append(f"{c:.3e}*x")
        else:
            partes.append(f"{c:.3e}*x^{p}")
    return " + ".join(partes)


def graficar(filas: List[dict], png_path: str) -> None:
    x = np.array([r["nW"] for r in filas], dtype=float)
    y_dp = np.array([r["t_dp"] for r in filas], dtype=float)
    y_gr = np.array([r["t_greedy"] for r in filas], dtype=float)

    # Probamos varios grados y nos quedamos con el mejor.
    fit_dp = ajustar_polinomio(x, y_dp, grados=(1, 2, 3))
    fit_gr = ajustar_polinomio(x, y_gr, grados=(1, 2, 3))

    # Adicionalmente, mostramos también la regresión lineal "teórica" para DP.
    coefs_dp_lin = np.polyfit(x, y_dp, 1)
    y_dp_lin_hat = np.polyval(coefs_dp_lin, x)
    ss_res_lin = np.sum((y_dp - y_dp_lin_hat) ** 2)
    ss_tot = np.sum((y_dp - np.mean(y_dp)) ** 2)
    r2_dp_lin = 1 - ss_res_lin / ss_tot if ss_tot > 0 else 1.0

    xs = np.linspace(x.min(), x.max(), 400)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(x, y_dp, color="#1f77b4", label="DP (datos)", zorder=3)
    ax.plot(xs, np.polyval(fit_dp["coefs"], xs),
            color="#1f77b4", linestyle="--",
            label=f"DP - regresión grado {fit_dp['grado']} (R²={fit_dp['r2']:.4f})")
    if fit_dp["grado"] != 1:
        ax.plot(xs, np.polyval(coefs_dp_lin, xs),
                color="#1f77b4", linestyle=":",
                label=f"DP - regresión lineal (R²={r2_dp_lin:.4f})")

    ax.scatter(x, y_gr, color="#d62728", label="Greedy (datos)", zorder=3)
    ax.plot(xs, np.polyval(fit_gr["coefs"], xs),
            color="#d62728", linestyle="--",
            label=f"Greedy - regresión grado {fit_gr['grado']} (R²={fit_gr['r2']:.4f})")

    ax.set_xlabel("Tamaño de entrada (n · W)")
    ax.set_ylabel("Tiempo de ejecución promedio (s)")
    ax.set_title("Coin Change: tiempos de ejecución DP vs. Greedy")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)

    print()
    print("Mejor ajuste polinomial DP:")
    print(f"  grado = {fit_dp['grado']}, R^2 = {fit_dp['r2']:.6f}")
    print(f"  p_dp(x) = {formatear_polinomio(fit_dp['coefs'])}")
    print("Regresión lineal forzada DP (referencia teórica):")
    print(f"  R^2 = {r2_dp_lin:.6f}")
    print(f"  p_dp_lin(x) = {formatear_polinomio(coefs_dp_lin)}")
    print("Mejor ajuste polinomial Greedy:")
    print(f"  grado = {fit_gr['grado']}, R^2 = {fit_gr['r2']:.6f}")
    print(f"  p_gr(x) = {formatear_polinomio(fit_gr['coefs'])}")
    print(f"\nGráfica guardada en: {png_path}")


# ----------------------------------------------------------------------------
# Evaluación de la calidad de la solución greedy
# ----------------------------------------------------------------------------

def evaluar_calidad():
    """Compara DP vs Greedy en sistemas canónicos y no canónicos."""
    print()
    print("=" * 60)
    print("Calidad de la solución greedy vs. solución óptima (DP)")
    print("=" * 60)
    casos = [
        ("Canónico USD",        [1, 5, 10, 25],      87),
        ("Canónico EUR",        [1, 2, 5, 10, 20, 50, 100, 200], 873),
        ("No canónico clásico", [1, 3, 4],            6),
        ("No canónico clásico", [1, 3, 4],           30),
        ("No canónico fuerte",  [1, 5, 10, 12, 25],  15),
        ("No canónico fuerte",  [1, 5, 10, 12, 25],  60),
        ("Tetra-canónico",      [1, 7, 24, 42],      48),
    ]
    for etiqueta, coins, W in casos:
        opt, _ = coin_change_dp(coins, W)
        gr, _ = coin_change_greedy(coins, W)
        if opt is None or gr is None:
            calidad = "N/A"
        elif opt == gr:
            calidad = "óptimo"
        else:
            calidad = f"subóptimo (greedy/óptimo = {gr}/{opt})"
        print(f"  [{etiqueta:>22}] coins={coins}, W={W:>4} -> DP={opt}, Greedy={gr}  {calidad}")


def analisis_ratio_aproximacion():
    """
    Sobre las mismas instancias del experimento principal, calcula el ratio
    greedy/óptimo cuando ambos completan W. Reporta:
      - Cuántas instancias greedy fue óptimo, subóptimo, y falló.
      - Ratio promedio y máximo.
    Guarda resultados en results/calidad_greedy.csv.
    """
    casos: List[Tuple[int, int]] = [
        (5,    100),
        (5,    500),
        (5,   1000),
        (8,   1000),
        (8,   2500),
        (10,  2500),
        (10,  5000),
        (12,  5000),
        (12, 10000),
        (15, 10000),
        (15, 20000),
        (20, 20000),
        (20, 40000),
        (25, 40000),
        (25, 80000),
    ]

    optimos = 0
    suboptimos = 0
    fallos = 0
    ratios: List[float] = []

    filas_csv: List[dict] = []

    print()
    print("=" * 70)
    print("Análisis del ratio de aproximación greedy/óptimo")
    print("=" * 70)
    print(f"{'n':>4} {'W':>8} {'DP':>6} {'Greedy':>8} {'Ratio':>8}  Estado")
    print("-" * 55)

    for i, (n, W) in enumerate(casos):
        coins = generar_caso(n, W, seed=42 + i)
        opt, _ = coin_change_dp(coins, W)
        gr, _ = coin_change_greedy(coins, W)

        if opt is None or gr is None:
            ratio = None
            estado = "fallo"
            fallos += 1
            ratio_str = "N/A"
        elif opt == gr:
            ratio = 1.0
            estado = "óptimo"
            optimos += 1
            ratios.append(ratio)
            ratio_str = f"{ratio:.4f}"
        else:
            ratio = gr / opt
            estado = "subóptimo"
            suboptimos += 1
            ratios.append(ratio)
            ratio_str = f"{ratio:.4f}"

        print(f"{n:>4} {W:>8} {str(opt):>6} {str(gr):>8} {ratio_str:>8}  {estado}")
        filas_csv.append({
            "n": n, "W": W, "dp": opt, "greedy": gr,
            "ratio_greedy_opt": ratio_str, "estado": estado,
        })

    print("-" * 55)
    print(f"  Óptimos:   {optimos}")
    print(f"  Subóptimos:{suboptimos}")
    print(f"  Fallos:    {fallos}")
    if ratios:
        print(f"  Ratio promedio: {sum(ratios)/len(ratios):.4f}")
        print(f"  Ratio máximo:   {max(ratios):.4f}")

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_dir = os.path.join(base, "results")
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "calidad_greedy.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["n", "W", "dp", "greedy", "ratio_greedy_opt", "estado"])
        writer.writeheader()
        writer.writerows(filas_csv)
    print(f"\nResultados guardados en: {csv_path}")


if __name__ == "__main__":
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base, "results", "benchmark_output.txt")

    with _Tee(out_path):
        correr_experimento()
        evaluar_calidad()
        analisis_ratio_aproximacion()

    print(f"Salida guardada en: {out_path}")
