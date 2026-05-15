"""
coin_change_greedy.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Heurística Greedy)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Heurística greedy para el problema del cambio de monedas.

    El algoritmo ordena las denominaciones de mayor a menor y, en cada paso,
    toma la mayor denominación que no exceda el residuo restante. Esta
    estrategia es óptima cuando el sistema de monedas es "canónico" (e.g.
    {1, 5, 10, 25} en USD), pero puede ser subóptima en sistemas no canónicos
    (e.g. {1, 3, 4} con W = 6: greedy produce 4+1+1 = 3 monedas; el óptimo
    es 3+3 = 2 monedas).

Complejidad temporal: O(n log n)  (dominada por el ordenamiento)
Complejidad espacial: O(n)

Importante:
    Este algoritmo NO siempre devuelve la solución óptima del Coin Change
    Problem genérico. La función devuelve None si no logra representar W
    con la heurística (lo cual NO implica que W sea irrepresentable: solo
    que la heurística falló).
"""

from __future__ import annotations
from typing import List, Optional, Tuple


def coin_change_greedy(
    coins: List[int],
    W: int,
    verbose: bool = False,
) -> Tuple[Optional[int], List[int]]:
    """Heurística greedy para el Coin Change Problem.

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
    (cantidad, monedas_usadas) :
        - cantidad: número de monedas usadas por la heurística, o None si la
          heurística no pudo representar W (incluso si DP sí podría).
        - monedas_usadas: lista de monedas elegidas (puede no ser óptima).
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

    if verbose:
        print(f"\n{'═' * 52}")
        print(f"  Greedy  coins={coins}  W={W}")
        print(f"{'═' * 52}")

    if W == 0:
        if verbose:
            print(f"  W=0  →  no se necesitan monedas")
            print(f"{'═' * 52}\n")
        return 0, []

    # Ordenamos descendentemente y eliminamos duplicados.
    sorted_coins = sorted(set(coins), reverse=True)

    if verbose:
        print(f"  Paso 1 — ordenar de mayor a menor: {sorted_coins}")
        print(f"  Paso 2 — tomar la mayor cantidad posible de cada denominación\n")
        print(f"  {'Moneda':>8}  {'¿c <= residuo?':>16}  {'Tomadas':>8}  {'Residuo':>8}")
        print(f"  {'─'*8}  {'─'*16}  {'─'*8}  {'─'*8}")

    used: List[int] = []
    remaining = W

    for c in sorted_coins:
        if c <= remaining:
            k = remaining // c
            used.extend([c] * k)
            remaining -= k * c
            if verbose:
                print(f"  {c:>8}  {'Sí':>16}  {k:>8}x  {remaining:>8}  → usadas: {used}")
        else:
            if verbose:
                print(f"  {c:>8}  {'No':>16}  {'—':>8}   {remaining:>8}  → saltar")
        if remaining == 0:
            break

    if verbose:
        print()

    if remaining != 0:
        if verbose:
            print(f"  ✗ No se pudo completar W={W} con la heurística.")
            print(f"    Residuo sin cubrir: {remaining}")
            print(f"    Monedas parciales:  {used}")
            print(f"{'═' * 52}\n")
        return None, used

    if verbose:
        print(f"  ✓ Completado: {len(used)} monedas  {used}")
        print(f"{'═' * 52}\n")

    return len(used), used


def _demo() -> None:
    """Demostración simple del comportamiento del algoritmo."""
    casos = [
        ([1, 5, 10, 25], 30),     # Greedy óptimo (canónico)
        ([1, 3, 4], 6),           # Greedy subóptimo: produce 3, óptimo es 2
        ([1, 5, 10, 12, 25], 15), # Greedy subóptimo: produce 6, óptimo es 2
        ([2, 4, 6], 7),           # Greedy falla (no representable)
    ]
    print("=== Resumen rápido ===")
    for coins, W in casos:
        cantidad, monedas = coin_change_greedy(coins, W)
        if cantidad is None:
            print(f"coins={coins}, W={W}  ->  greedy falló  (parcial: {monedas})")
        else:
            print(f"coins={coins}, W={W}  ->  {cantidad} monedas  {monedas}")

    print("\n=== Paso a paso (verbose) ===")
    coin_change_greedy([1, 3, 4], 6, verbose=True)
    coin_change_greedy([2, 4, 6], 7, verbose=True)


if __name__ == "__main__":
    _demo()
