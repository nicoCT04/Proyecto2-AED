"""
analisis_calidad.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Análisis de Calidad)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Análisis estadístico y visual del ratio de aproximación greedy/óptimo a
    partir del archivo results/calidad_greedy.csv generado por benchmark.py.

    Produce tres gráficas y un resumen estadístico:
      1) Barras de ratio greedy/óptimo por instancia (ordenadas).
      2) Histograma de la distribución de ratios.
      3) Scatter DP vs. Greedy (cantidad de monedas), con línea y=x.

    También imprime una tabla de estadísticas descriptivas y una
    categorización por severidad (aceptable / malo / catastrófico).

Uso:
    python src/analisis_calidad.py

Requisitos:
    Haber corrido previamente benchmark.py para que exista el CSV de entrada.
"""

from __future__ import annotations
import csv
import os
import sys
from typing import List, Dict

import numpy as np
import matplotlib
matplotlib.use("Agg")  # backend sin GUI para guardar imágenes
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------------
# Carga de datos
# ----------------------------------------------------------------------------

def cargar_csv(csv_path: str) -> List[Dict]:
    """Lee calidad_greedy.csv y devuelve una lista de diccionarios tipados."""
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(
            f"No se encontró {csv_path}. Corré primero 'python src/benchmark.py'."
        )

    filas: List[Dict] = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            filas.append({
                "n": int(r["n"]),
                "W": int(r["W"]),
                "dp": int(r["dp"]),
                "greedy": int(r["greedy"]),
                "ratio": float(r["ratio_greedy_opt"]),
                "estado": r["estado"],
                "nW": int(r["n"]) * int(r["W"]),
            })
    if not filas:
        raise ValueError(f"El archivo {csv_path} está vacío.")
    return filas


# ----------------------------------------------------------------------------
# Estadísticas descriptivas
# ----------------------------------------------------------------------------

def calcular_estadisticas(filas: List[Dict]) -> Dict:
    """Calcula estadísticas descriptivas del ratio greedy/óptimo."""
    ratios = np.array([f["ratio"] for f in filas], dtype=float)
    return {
        "n_total":   len(ratios),
        "media":     float(np.mean(ratios)),
        "mediana":   float(np.median(ratios)),
        "std":       float(np.std(ratios, ddof=1)) if len(ratios) > 1 else 0.0,
        "minimo":    float(np.min(ratios)),
        "maximo":    float(np.max(ratios)),
        "p25":       float(np.percentile(ratios, 25)),
        "p75":       float(np.percentile(ratios, 75)),
        "p90":       float(np.percentile(ratios, 90)),
    }


def categorizar_por_severidad(filas: List[Dict]) -> Dict[str, int]:
    """Cuenta cuántos casos caen en cada categoría de severidad."""
    cat = {"óptimo (=1.0)": 0,
           "aceptable (1.0,1.5]": 0,
           "malo (1.5,10]": 0,
           "catastrófico (>10)": 0}
    for f in filas:
        r = f["ratio"]
        if r <= 1.0:
            cat["óptimo (=1.0)"] += 1
        elif r <= 1.5:
            cat["aceptable (1.0,1.5]"] += 1
        elif r <= 10:
            cat["malo (1.5,10]"] += 1
        else:
            cat["catastrófico (>10)"] += 1
    return cat


def imprimir_reporte(filas: List[Dict]) -> None:
    """Imprime estadísticas, categorización y casos notables."""
    stats = calcular_estadisticas(filas)
    cat = categorizar_por_severidad(filas)

    print()
    print("=" * 70)
    print("Estadísticas descriptivas del ratio greedy/óptimo")
    print("=" * 70)
    print(f"  Instancias totales:        {stats['n_total']}")
    print(f"  Media:                     {stats['media']:.4f}")
    print(f"  Mediana:                   {stats['mediana']:.4f}")
    print(f"  Desviación estándar:       {stats['std']:.4f}")
    print(f"  Mínimo:                    {stats['minimo']:.4f}")
    print(f"  Percentil 25:              {stats['p25']:.4f}")
    print(f"  Percentil 75:              {stats['p75']:.4f}")
    print(f"  Percentil 90:              {stats['p90']:.4f}")
    print(f"  Máximo:                    {stats['maximo']:.4f}")

    print()
    print("=" * 70)
    print("Categorización por severidad")
    print("=" * 70)
    total = stats["n_total"]
    for etiqueta, count in cat.items():
        pct = 100 * count / total if total else 0
        print(f"  {etiqueta:<25}  {count:>3} instancias  ({pct:5.1f} %)")

    print()
    print("=" * 70)
    print("Casos notables")
    print("=" * 70)
    peor = max(filas, key=lambda f: f["ratio"])
    mejor = min(filas, key=lambda f: f["ratio"])
    print(f"  PEOR caso  : n={peor['n']:>3}, W={peor['W']:>6}, "
          f"DP={peor['dp']}, Greedy={peor['greedy']}, ratio={peor['ratio']:.4f}")
    print(f"  MEJOR caso : n={mejor['n']:>3}, W={mejor['W']:>6}, "
          f"DP={mejor['dp']}, Greedy={mejor['greedy']}, ratio={mejor['ratio']:.4f}")


# ----------------------------------------------------------------------------
# Gráfica 1: barras de ratio por instancia (ordenadas)
# ----------------------------------------------------------------------------

def grafica_ratio_barras(filas: List[Dict], png_path: str) -> None:
    """Barras horizontales del ratio por instancia, ordenadas asc."""
    ordenadas = sorted(filas, key=lambda f: f["ratio"])
    etiquetas = [f"n={f['n']}, W={f['W']}" for f in ordenadas]
    ratios = [f["ratio"] for f in ordenadas]

    colores = []
    for r in ratios:
        if r <= 1.0:
            colores.append("#2ca02c")     # verde - óptimo
        elif r <= 1.5:
            colores.append("#bcbd22")     # amarillo verdoso - aceptable
        elif r <= 10:
            colores.append("#ff7f0e")     # naranja - malo
        else:
            colores.append("#d62728")     # rojo - catastrófico

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(etiquetas, ratios, color=colores, edgecolor="black", linewidth=0.5)

    # Línea de referencia en ratio=1 (greedy óptimo)
    ax.axvline(x=1.0, color="black", linestyle="--", linewidth=1,
               label="Óptimo (ratio = 1.0)")

    # Etiquetas numéricas al final de cada barra
    for bar, ratio in zip(bars, ratios):
        ax.text(bar.get_width() * 1.02, bar.get_y() + bar.get_height() / 2,
                f"{ratio:.2f}×", va="center", fontsize=8)

    ax.set_xlabel("Ratio greedy / óptimo")
    ax.set_ylabel("Instancia (n, W)")
    ax.set_title("Ratio de aproximación greedy/óptimo por instancia\n"
                 "(15 sistemas no canónicos aleatorios)")
    ax.set_xscale("log")
    ax.grid(True, axis="x", linestyle=":", alpha=0.6)
    ax.legend(loc="lower right")
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)
    print(f"  Guardada: {png_path}")


# ----------------------------------------------------------------------------
# Gráfica 2: histograma de ratios
# ----------------------------------------------------------------------------

def grafica_histograma(filas: List[Dict], png_path: str) -> None:
    """Histograma de la distribución de ratios."""
    ratios = np.array([f["ratio"] for f in filas])

    fig, ax = plt.subplots(figsize=(9, 6))

    # Bins logarítmicos (porque los ratios cubren varios órdenes de magnitud)
    bins = np.logspace(np.log10(max(ratios.min(), 0.5)),
                       np.log10(ratios.max()) + 0.1, 12)
    ax.hist(ratios, bins=bins, color="#1f77b4",
            edgecolor="black", alpha=0.8)

    ax.axvline(x=1.0, color="green", linestyle="--", linewidth=1.5,
               label="Óptimo (ratio = 1.0)")
    ax.axvline(x=float(np.mean(ratios)), color="red", linestyle="-.",
               linewidth=1.5, label=f"Media = {np.mean(ratios):.2f}")
    ax.axvline(x=float(np.median(ratios)), color="orange", linestyle=":",
               linewidth=1.5, label=f"Mediana = {np.median(ratios):.2f}")

    ax.set_xscale("log")
    ax.set_xlabel("Ratio greedy / óptimo (escala log)")
    ax.set_ylabel("Frecuencia (cantidad de instancias)")
    ax.set_title("Distribución del ratio de aproximación greedy/óptimo")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend()
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)
    print(f"  Guardada: {png_path}")


# ----------------------------------------------------------------------------
# Gráfica 3: DP vs Greedy (scatter)
# ----------------------------------------------------------------------------

def grafica_dp_vs_greedy(filas: List[Dict], png_path: str) -> None:
    """Scatter de DP (eje X) vs. Greedy (eje Y) con línea y=x."""
    dp = np.array([f["dp"] for f in filas], dtype=float)
    gr = np.array([f["greedy"] for f in filas], dtype=float)

    fig, ax = plt.subplots(figsize=(9, 7))

    # Línea de referencia y = x (greedy = óptimo)
    lim = max(dp.max(), gr.max()) * 1.2
    xs = np.linspace(0.5, lim, 200)
    ax.plot(xs, xs, color="green", linestyle="--", linewidth=1.5,
            label="y = x  (greedy óptimo)")

    # Puntos
    sc = ax.scatter(dp, gr, c=[f["ratio"] for f in filas],
                    cmap="YlOrRd", s=80, edgecolor="black",
                    linewidth=0.5, zorder=3)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Ratio greedy / óptimo")

    # Etiqueta del peor caso
    peor_idx = int(np.argmax([f["ratio"] for f in filas]))
    ax.annotate(f"Peor caso\n(ratio {filas[peor_idx]['ratio']:.1f}×)",
                xy=(dp[peor_idx], gr[peor_idx]),
                xytext=(dp[peor_idx] * 1.5, gr[peor_idx] * 1.2),
                arrowprops=dict(arrowstyle="->", color="red"),
                fontsize=9, color="red")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Cantidad óptima de monedas (DP)")
    ax.set_ylabel("Cantidad de monedas usadas por Greedy")
    ax.set_title("DP vs. Greedy: cantidad de monedas por instancia\n"
                 "Puntos por encima de la línea = greedy subóptimo")
    ax.grid(True, linestyle=":", alpha=0.6, which="both")
    ax.legend(loc="upper left")
    fig.tight_layout()
    fig.savefig(png_path, dpi=150)
    plt.close(fig)
    print(f"  Guardada: {png_path}")


# ----------------------------------------------------------------------------
# Guardado de estadísticas en CSV (datos crudos para el informe)
# ----------------------------------------------------------------------------

def exportar_estadisticas_csv(filas: List[Dict], csv_path: str) -> None:
    """Exporta estadísticas y categorización a un CSV legible para el informe."""
    stats = calcular_estadisticas(filas)
    cat = categorizar_por_severidad(filas)
    peor = max(filas, key=lambda f: f["ratio"])
    mejor = min(filas, key=lambda f: f["ratio"])

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["metrica", "valor"])
        w.writerow(["n_instancias", stats["n_total"]])
        w.writerow(["ratio_medio", f"{stats['media']:.4f}"])
        w.writerow(["ratio_mediana", f"{stats['mediana']:.4f}"])
        w.writerow(["ratio_desv_std", f"{stats['std']:.4f}"])
        w.writerow(["ratio_minimo", f"{stats['minimo']:.4f}"])
        w.writerow(["ratio_maximo", f"{stats['maximo']:.4f}"])
        w.writerow(["ratio_p25", f"{stats['p25']:.4f}"])
        w.writerow(["ratio_p75", f"{stats['p75']:.4f}"])
        w.writerow(["ratio_p90", f"{stats['p90']:.4f}"])
        w.writerow([])
        w.writerow(["categoria", "instancias"])
        for k, v in cat.items():
            w.writerow([k, v])
        w.writerow([])
        w.writerow(["caso", "n", "W", "dp", "greedy", "ratio"])
        w.writerow(["peor", peor["n"], peor["W"],
                    peor["dp"], peor["greedy"], f"{peor['ratio']:.4f}"])
        w.writerow(["mejor", mejor["n"], mejor["W"],
                    mejor["dp"], mejor["greedy"], f"{mejor['ratio']:.4f}"])

    print(f"  Estadísticas exportadas: {csv_path}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main() -> int:
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base, "results")
    csv_in = os.path.join(results_dir, "calidad_greedy.csv")

    print("=" * 70)
    print("Análisis de calidad: ratio greedy/óptimo")
    print("=" * 70)
    print(f"Leyendo: {csv_in}")

    try:
        filas = cargar_csv(csv_in)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Instancias cargadas: {len(filas)}")

    # Reporte por consola
    imprimir_reporte(filas)

    # Gráficas
    print()
    print("=" * 70)
    print("Generando gráficas")
    print("=" * 70)
    grafica_ratio_barras(filas, os.path.join(results_dir, "calidad_ratio_barras.png"))
    grafica_histograma(filas, os.path.join(results_dir, "calidad_histograma.png"))
    grafica_dp_vs_greedy(filas, os.path.join(results_dir, "calidad_dp_vs_greedy.png"))

    # Estadísticas en CSV
    print()
    print("=" * 70)
    print("Exportando estadísticas")
    print("=" * 70)
    exportar_estadisticas_csv(filas, os.path.join(results_dir, "calidad_estadisticas.csv"))

    print()
    print("Análisis completado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())