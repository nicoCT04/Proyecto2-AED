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
from typing import List

from coin_change_base import (
    CoinChangeSolver,
    Resultado,
    ejecutar_cli,
    ejecutar_demo,
)


# ===========================================================================
# Núcleo del algoritmo
# ===========================================================================

class GreedySolver(CoinChangeSolver):
    """Resolvedor del Coin Change Problem por heurística Greedy."""

    nombre = "Greedy"

    def _algoritmo(self, coins: List[int], W: int, verbose: bool) -> Resultado:
        if W == 0:
            if verbose:
                print(f"  W=0  →  no se necesitan monedas")
            return 0, []

        # Ordenamos descendentemente y eliminamos duplicados.
        sorted_coins = sorted(set(coins), reverse=True)

        if verbose:
            self._log_encabezado_tabla(sorted_coins)

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

        if remaining != 0:
            if verbose:
                print(f"\n  ✗ No se pudo completar W={W} con la heurística.")
                print(f"    Residuo sin cubrir: {remaining}")
                print(f"    Monedas parciales:  {used}")
            return None, used

        if verbose:
            print(f"\n  ✓ Completado: {len(used)} monedas  {used}")

        return len(used), used

    # ----- helpers de presentación verbose (no afectan el algoritmo) -----

    @staticmethod
    def _log_encabezado_tabla(sorted_coins: List[int]) -> None:
        print(f"  Paso 1 — ordenar de mayor a menor: {sorted_coins}")
        print(f"  Paso 2 — tomar la mayor cantidad posible de cada denominación\n")
        print(f"  {'Moneda':>8}  {'¿c <= residuo?':>16}  {'Tomadas':>8}  {'Residuo':>8}")
        print(f"  {'─'*8}  {'─'*16}  {'─'*8}  {'─'*8}")


# ===========================================================================
# API pública (función) y CLI
# ===========================================================================

_solver = GreedySolver()


def coin_change_greedy(coins: List[int], W: int, verbose: bool = False) -> Resultado:
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
    return _solver.resolver(coins, W, verbose=verbose)


def _demo() -> None:
    casos = [
        ([1, 5, 10, 25], 30),     # Greedy óptimo (canónico)
        ([1, 3, 4], 6),           # Greedy subóptimo: produce 3, óptimo es 2
        ([1, 5, 10, 12, 25], 15), # Greedy subóptimo: produce 6, óptimo es 2
        ([2, 4, 6], 7),           # Greedy falla (no representable)
    ]
    casos_verbose = [
        ([1, 3, 4], 6),
        ([2, 4, 6], 7),
    ]
    ejecutar_demo(coin_change_greedy, casos, casos_verbose,
                  etiqueta_fallo="greedy falló", mostrar_parcial=True)


if __name__ == "__main__":
    ejecutar_cli(
        descripcion="Coin Change — Heurística Greedy",
        ejemplo="Ejemplo: python coin_change_greedy.py --coins 1 3 4 --W 6 --verbose",
        solver_fn=coin_change_greedy,
        fn_demo=_demo,
        etiqueta_fallo="greedy falló",
        mostrar_parcial=True,
    )
