"""
coin_change_dp.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Programación Dinámica)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Implementación bottom-up del Coin Change Problem usando programación
    dinámica. Dado un conjunto de denominaciones C = {c1, ..., cn} y un
    monto objetivo W, encuentra la cantidad mínima de monedas que suman
    exactamente W.

    Recurrencia:
        dp[0] = 0
        dp[w] = min{ dp[w - c] + 1  para todo c en C tal que c <= w }
        dp[w] = INF   si ninguna denominación permite avanzar.

    Reconstrucción: el arreglo parent[w] guarda la denominación elegida
    que produjo el mínimo en dp[w], permitiendo reconstruir la solución
    en O(W) recorriendo desde W hasta 0.

    Complejidad temporal: O(n * W) — pseudo-polinomial.
    Complejidad espacial: O(W) para dp[] y parent[].

Casos borde:
    - W = 0  -> (0, [])
    - W no representable  -> (None, [])
"""

from __future__ import annotations
from typing import List, Optional, Tuple
import math


def _dp_str(dp: List[float], W: int) -> str:
    """Representa la tabla dp como string, mostrando ∞ en vez de inf."""
    partes = []
    for i, v in enumerate(dp):
        marca = " <" if i == W else ""
        partes.append(f"  {i}: {'∞' if v == math.inf else int(v)}{marca}")
    return "\n".join(partes)


def coin_change_dp(
    coins: List[int],
    W: int,
    verbose: bool = False,
) -> Tuple[Optional[int], List[int]]:
    """Resuelve el Coin Change Problem usando programación dinámica bottom-up.

    Parámetros
    ----------
    coins : list[int]
        Lista de denominaciones disponibles (enteros positivos).
    W : int
        Monto objetivo (entero no negativo).
    verbose : bool
        Si es True, imprime el paso a paso del algoritmo.

    Devuelve
    --------
    (cantidad_minima, monedas_usadas) :
        - cantidad_minima: número mínimo de monedas, o None si no es alcanzable.
        - monedas_usadas: lista con las monedas que conforman la solución.
    """
    if not isinstance(W, int):
        raise TypeError("W debe ser entero.")
    if not isinstance(coins, list):
        raise TypeError("coins debe ser list.")
    if len(coins) == 0:
        raise ValueError("coins no puede estar vacío.")
    if any(not isinstance(c, int) for c in coins):
        raise TypeError("Todas las denominaciones deben ser enteros.")
    if W < 0:
        raise ValueError("W debe ser un entero no negativo.")
    if any(c <= 0 for c in coins):
        raise ValueError("Todas las denominaciones deben ser enteros positivos.")

    SEP = "─" * 52

    if verbose:
        print(f"\n{'═' * 52}")
        print(f"  DP  coins={coins}  W={W}")
        print(f"{'═' * 52}")
        print(f"  Caso base: dp[0] = 0  (sumar 0 no requiere monedas)")
        print(f"  Resto de la tabla inicializada en ∞ (inalcanzable)\n")

    INF = math.inf
    dp: List[float] = [INF] * (W + 1)
    dp[0] = 0
    parent: List[int] = [-1] * (W + 1)

    for w in range(1, W + 1):
        if verbose:
            print(f"  {SEP}")
            print(f"  Llenando dp[{w}]  (mejor hasta ahora: ∞)")

        for c in coins:
            moneda_alcanzable = c <= w
            if moneda_alcanzable:
                mejora_el_resultado = dp[w - c] + 1 < dp[w]
                if verbose:
                    candidato = int(dp[w - c]) + 1 if dp[w - c] != INF else "∞+1"
                    actual    = "∞" if dp[w] == INF else int(dp[w])
                    simbolo   = "✓ actualiza" if mejora_el_resultado else "✗ no mejora"
                    print(f"    c={c:>3}  dp[{w}-{c}]+1 = {candidato}  vs  dp[{w}]={actual}  → {simbolo}")
                if mejora_el_resultado:
                    dp[w] = dp[w - c] + 1
                    parent[w] = c
            else:
                if verbose:
                    print(f"    c={c:>3}  {c} > {w}, moneda no alcanzable  → saltar")

        if verbose:
            resultado = "∞" if dp[w] == INF else int(dp[w])
            print(f"  → dp[{w}] = {resultado}")

    if verbose:
        print(f"\n  {'═' * 48}")
        print(f"  Tabla dp final:")
        print(_dp_str(dp, W))
        print()

    if dp[W] == INF:
        if verbose:
            print(f"  dp[{W}] = ∞  →  W={W} no es representable con {coins}")
            print(f"{'═' * 52}\n")
        return None, []

    # Reconstrucción de la solución.
    used: List[int] = []
    w = W
    if verbose:
        print(f"  Reconstrucción (siguiendo parent[] desde w={W} hasta 0):")
    while w > 0:
        c = parent[w]
        used.append(c)
        if verbose:
            print(f"    w={w}  →  usó moneda {c}  →  w={w - c}")
        w -= c

    if verbose:
        print(f"\n  Resultado: {int(dp[W])} monedas  {used}")
        print(f"{'═' * 52}\n")

    return int(dp[W]), used


def _demo() -> None:
    """Demostración simple del comportamiento del algoritmo."""
    casos = [
        ([1, 5, 10, 25], 30),     # Sistema "canónico" (USD)
        ([1, 3, 4], 6),           # Caso clásico donde greedy falla
        ([1, 5, 10, 12, 25], 15), # Otro caso donde greedy falla
        ([2, 4, 6], 7),           # No representable
    ]
    print("=== Resumen rápido ===")
    for coins, W in casos:
        cantidad, monedas = coin_change_dp(coins, W)
        if cantidad is None:
            print(f"coins={coins}, W={W}  ->  no representable")
        else:
            print(f"coins={coins}, W={W}  ->  {cantidad} monedas  {monedas}")

    print("\n=== Paso a paso (verbose) ===")
    coin_change_dp([1, 3, 4], 6, verbose=True)
    coin_change_dp([2, 4, 6], 7, verbose=True)


if __name__ == "__main__":
    _demo()
