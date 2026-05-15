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

from coin_change_base import (
    CoinChangeSolver,
    Resultado,
    SEPARADOR_SIMPLE,
    ejecutar_cli,
    ejecutar_demo,
)


# ===========================================================================
# Núcleo del algoritmo
# ===========================================================================

class DPSolver(CoinChangeSolver):
    """Resolvedor del Coin Change Problem por Programación Dinámica."""

    nombre = "DP"

    def _algoritmo(self, coins: List[int], W: int, verbose: bool) -> Resultado:
        INF = math.inf

        # dp[w] = mínima cantidad de monedas para sumar exactamente w.
        dp: List[float] = [INF] * (W + 1)
        dp[0] = 0
        # parent[w] = denominación elegida que produjo el óptimo en dp[w].
        parent: List[int] = [-1] * (W + 1)

        if verbose:
            print(f"  Caso base: dp[0] = 0  (sumar 0 no requiere monedas)")
            print(f"  Resto de la tabla inicializada en ∞ (inalcanzable)\n")

        for w in range(1, W + 1):
            if verbose:
                print(f"  {SEPARADOR_SIMPLE}")
                print(f"  Llenando dp[{w}]  (mejor hasta ahora: ∞)")

            for c in coins:
                moneda_alcanzable = c <= w
                if moneda_alcanzable:
                    mejora_el_resultado = dp[w - c] + 1 < dp[w]
                    if verbose:
                        self._log_intento(w, c, dp, mejora_el_resultado)
                    if mejora_el_resultado:
                        dp[w] = dp[w - c] + 1
                        parent[w] = c
                else:
                    if verbose:
                        print(f"    c={c:>3}  {c} > {w}, moneda no alcanzable  → saltar")

            if verbose:
                actual = "∞" if dp[w] == INF else int(dp[w])
                print(f"  → dp[{w}] = {actual}")

        if verbose:
            self._log_tabla_final(dp, W)

        if dp[W] == INF:
            if verbose:
                print(f"  dp[{W}] = ∞  →  W={W} no es representable con {coins}")
            return None, []

        # Reconstrucción siguiendo parent[] desde W hasta 0.
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

        return int(dp[W]), used

    # ----- helpers de presentación verbose (no afectan el algoritmo) -----

    @staticmethod
    def _log_intento(w: int, c: int, dp: List[float], mejora: bool) -> None:
        candidato = int(dp[w - c]) + 1 if dp[w - c] != math.inf else "∞+1"
        actual    = "∞" if dp[w] == math.inf else int(dp[w])
        simbolo   = "✓ actualiza" if mejora else "✗ no mejora"
        print(f"    c={c:>3}  dp[{w}-{c}]+1 = {candidato}  vs  dp[{w}]={actual}  → {simbolo}")

    @staticmethod
    def _log_tabla_final(dp: List[float], W: int) -> None:
        print(f"\n  {'═' * 48}")
        print(f"  Tabla dp final:")
        for i, v in enumerate(dp):
            marca = " <" if i == W else ""
            print(f"  {i}: {'∞' if v == math.inf else int(v)}{marca}")
        print()


# ===========================================================================
# API pública (función) y CLI
# ===========================================================================

_solver = DPSolver()


def coin_change_dp(coins: List[int], W: int, verbose: bool = False) -> Resultado:
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
    return _solver.resolver(coins, W, verbose=verbose)


def _demo() -> None:
    casos = [
        ([1, 5, 10, 25], 30),     # Sistema "canónico" (USD)
        ([1, 3, 4], 6),           # Caso clásico donde greedy falla
        ([1, 5, 10, 12, 25], 15), # Otro caso donde greedy falla
        ([2, 4, 6], 7),           # No representable
    ]
    casos_verbose = [
        ([1, 3, 4], 6),
        ([2, 4, 6], 7),
    ]
    ejecutar_demo(coin_change_dp, casos, casos_verbose,
                  etiqueta_fallo="no representable", mostrar_parcial=False)


if __name__ == "__main__":
    ejecutar_cli(
        descripcion="Coin Change — Programación Dinámica",
        ejemplo="Ejemplo: python coin_change_dp.py --coins 1 3 4 --W 6 --verbose",
        solver_fn=coin_change_dp,
        fn_demo=_demo,
        etiqueta_fallo="no representable",
        mostrar_parcial=False,
    )
