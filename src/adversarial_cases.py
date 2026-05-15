"""
adversarial_cases.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Análisis de Casos Adversariales)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Genera y evalúa sistemas de monedas donde la heurística greedy falla
    catastróficamente, cuantificando el ratio greedy/óptimo. El ratio
    indica cuántas veces más monedas usa greedy respecto al óptimo.

    Patrón adversarial clave: el sistema [1, k-1, k] con W=2*(k-1) hace
    que greedy elija k + (k-2)*1 = k-1 monedas, mientras el óptimo es
    solo 2 monedas de denominación k-1. El ratio crece con k.
"""

from __future__ import annotations
from typing import List, Optional

from coin_change_dp import coin_change_dp
from coin_change_greedy import coin_change_greedy


def evaluar_caso(coins: List[int], W: int) -> dict:
    """Evalúa un par (coins, W) con DP y greedy y calcula el ratio.

    Parámetros
    ----------
    coins : list[int]
        Lista de denominaciones.
    W : int
        Monto objetivo.

    Devuelve
    --------
    dict con claves: coins, W, dp, greedy, ratio, es_suboptimo.
    """
    opt, _ = coin_change_dp(coins, W)
    gr, _ = coin_change_greedy(coins, W)

    if opt is None or gr is None:
        ratio = None
    elif opt == 0:
        ratio = 1.0
    else:
        ratio = gr / opt

    es_suboptimo = (opt is not None and gr is not None and gr > opt)

    return {
        "coins": coins,
        "W": W,
        "dp": opt,
        "greedy": gr,
        "ratio": ratio,
        "es_suboptimo": es_suboptimo,
    }


def generar_adversarial_simple(k: int) -> List[int]:
    """Genera el sistema [1, k-1, k] que engaña al greedy en W=2*(k-1).

    Parámetros
    ----------
    k : int
        Parámetro de la familia adversarial (k >= 3).

    Devuelve
    --------
    list[int] con denominaciones [1, k-1, k].
    """
    if k < 3:
        raise ValueError("k debe ser >= 3 para producir un sistema no trivial.")
    return [1, k - 1, k]


def main() -> None:
    """Imprime tabla de casos adversariales con ratios greedy/óptimo."""
    casos_fijos = [
        ([1, 3, 4],           6,  "clásico [1,3,4]"),
        ([1, 5, 10, 12, 25],  15, "mixto W=15"),
        ([1, 5, 10, 12, 25],  30, "mixto W=30"),
        ([1, 5, 10, 12, 25],  60, "mixto W=60"),
        ([1, 7, 24, 42],      48, "tetra-canónico W=48"),
    ]

    resultados = []
    for coins, W, etiqueta in casos_fijos:
        r = evaluar_caso(coins, W)
        r["etiqueta"] = etiqueta
        resultados.append(r)

    # Series generadas con el patrón [1, k-1, k]
    for k in [5, 10, 20, 50, 100]:
        coins = generar_adversarial_simple(k)
        W = 2 * (k - 1)
        r = evaluar_caso(coins, W)
        r["etiqueta"] = f"[1,{k-1},{k}] W={W}"
        resultados.append(r)

    # Ordenar por ratio descendente (None al final)
    resultados.sort(key=lambda x: (x["ratio"] is None, -(x["ratio"] or 0)))

    print(f"{'Etiqueta':<28} {'coins':<20} {'W':>6} {'DP':>5} {'Greedy':>7} {'Ratio':>7}")
    print("-" * 80)
    for r in resultados:
        coins_str = str(r["coins"])
        ratio_str = f"{r['ratio']:.2f}" if r["ratio"] is not None else "N/A"
        print(f"  {r['etiqueta']:<26} {coins_str:<20} {r['W']:>6} "
              f"{str(r['dp']):>5} {str(r['greedy']):>7} {ratio_str:>7}")


if __name__ == "__main__":
    main()
