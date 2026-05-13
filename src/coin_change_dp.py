from __future__ import annotations
from typing import List, Optional, Tuple
import math


def coin_change_dp(coins: List[int], W: int) -> Tuple[Optional[int], List[int]]:
    """Resuelve el Coin Change Problem usando programación dinámica bottom-up.

    Parámetros
    ----------
    coins : list[int]
        Lista de denominaciones disponibles (enteros positivos).
    W : int
        Monto objetivo (entero no negativo).

    Devuelve
    --------
    (cantidad_minima, monedas_usadas) :
        - cantidad_minima: número mínimo de monedas, o None si no es alcanzable.
        - monedas_usadas: lista con las monedas que conforman la solución.
    """
    if W < 0:
        raise ValueError("W debe ser un entero no negativo.")
    if any(c <= 0 for c in coins):
        raise ValueError("Todas las denominaciones deben ser enteros positivos.")

    INF = math.inf
    # dp[w] = mínima cantidad de monedas para sumar exactamente w.
    dp: List[float] = [INF] * (W + 1)
    dp[0] = 0
    # parent[w] = denominación elegida que produjo el óptimo en dp[w].
    parent: List[int] = [-1] * (W + 1)

    for w in range(1, W + 1):
        for c in coins:
            if c <= w and dp[w - c] + 1 < dp[w]:
                dp[w] = dp[w - c] + 1
                parent[w] = c

    if dp[W] == INF:
        return None, []

    # Reconstrucción de la solución.
    used: List[int] = []
    w = W
    while w > 0:
        c = parent[w]
        used.append(c)
        w -= c

    return int(dp[W]), used


def _demo() -> None:
    """Demostración simple del comportamiento del algoritmo."""
    casos = [
        ([1, 5, 10, 25], 30),     # Sistema "canónico" (USD)
        ([1, 3, 4], 6),           # Caso clásico donde greedy falla
        ([1, 5, 10, 12, 25], 15), # Otro caso donde greedy falla
        ([2, 4, 6], 7),           # No representable
    ]
    for coins, W in casos:
        cantidad, monedas = coin_change_dp(coins, W)
        if cantidad is None:
            print(f"coins={coins}, W={W}  ->  no representable")
        else:
            print(f"coins={coins}, W={W}  ->  {cantidad} monedas  {monedas}")


if __name__ == "__main__":
    _demo()