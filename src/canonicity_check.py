"""
canonicity_check.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Verificador de Canonicidad)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Implementación del test de Pearson (2005) para decidir en tiempo
    polinomial si un sistema de monedas es canónico. Un sistema es canónico
    si y solo si la heurística greedy produce la solución óptima para
    TODO valor de W.

    Teorema de Pearson: basta verificar los valores W en el rango
        [c[2] + 1,  c[-2] + c[-1]]
    (donde c está ordenado ascendentemente) para decidir canonicidad.
    Este rango es polinomial en las denominaciones.

Referencia:
    Pearson, D. (2005). A polynomial-time algorithm for the change-making
    problem. Operations Research Letters, 33(3), 231-234.
"""

from __future__ import annotations
from typing import List, Optional, Tuple

from coin_change_dp import coin_change_dp
from coin_change_greedy import coin_change_greedy


def es_canonico(coins: List[int]) -> Tuple[bool, Optional[int]]:
    """Verifica si el sistema de monedas es canónico (greedy óptimo para todo W).

    Parámetros
    ----------
    coins : list[int]
        Lista de denominaciones disponibles (enteros positivos).

    Devuelve
    --------
    (True, None)           si el sistema es canónico.
    (False, contraejemplo) si NO es canónico, donde `contraejemplo` es un
                           valor W donde greedy difiere de DP.
    """
    if not isinstance(coins, list):
        raise TypeError("coins debe ser list.")
    if len(coins) == 0:
        raise ValueError("coins no puede estar vacío.")
    if any(not isinstance(c, int) for c in coins):
        raise TypeError("Todas las denominaciones deben ser enteros.")
    if any(c <= 0 for c in coins):
        raise ValueError("Todas las denominaciones deben ser enteros positivos.")

    c = sorted(set(coins))

    if c[0] != 1:
        print(f"  [Advertencia] El test de Pearson asume que la moneda 1 está presente. "
              f"Denominación mínima encontrada: {c[0]}.")

    # Con ≤2 denominaciones distintas (la primera siendo 1), el sistema es canónico.
    if len(c) < 3:
        return True, None

    # Rango de Pearson: verificar W en [c[2]+1, c[-2]+c[-1]]
    w_min = c[2] + 1
    w_max = c[-2] + c[-1]

    for w in range(w_min, w_max + 1):
        opt, _ = coin_change_dp(c, w)
        gr, _ = coin_change_greedy(c, w)
        if opt is None:
            # W no representable: greedy tampoco puede ser mejor, ignorar.
            continue
        if gr is None or gr != opt:
            return False, w

    return True, None


def _demo() -> None:
    """Demostración del verificador con sistemas canónicos y no canónicos."""
    casos = [
        ("USD canónico",        [1, 5, 10, 25]),
        ("EUR canónico",        [1, 2, 5, 10, 20, 50, 100, 200]),
        ("No canónico clásico", [1, 3, 4]),
        ("No canónico mixto",   [1, 5, 10, 12, 25]),
        ("No canónico fuerte",  [1, 7, 24, 42]),
    ]

    print()
    print("  ¿Qué significa que un sistema sea canónico?")
    print("  Un sistema es CANÓNICO si greedy siempre produce la solución")
    print("  óptima, sin importar el valor de W. Si existe aunque sea un")
    print("  solo W donde greedy falla, el sistema NO es canónico.")
    print()

    for nombre, coins in casos:
        canonico, contra = es_canonico(coins)

        print(f"{'═' * 56}")
        print(f"  {nombre}")
        print(f"  Denominaciones: {coins}")

        if canonico:
            print(f"  Canónico:       Sí")
            print(f"  Razón:          greedy es óptimo para todo W posible")
        else:
            opt, _ = coin_change_dp(coins, contra)
            gr, _  = coin_change_greedy(coins, contra)
            ratio  = f"{gr}/{opt} = {gr/opt:.1f}×" if opt and gr else "N/A"
            print(f"  Canónico:       No")
            print(f"  Contraejemplo:  W={contra}")
            print(f"    DP    → {opt} monedas  (óptimo)")
            print(f"    Greedy→ {gr} monedas  (subóptimo, ratio {ratio})")
            print(f"  Razón:  greedy elige la moneda más grande disponible")
            print(f"          y no puede retroceder, quedando atrapado en")
            print(f"          una combinación peor que la óptima.")

    print(f"{'═' * 56}")


if __name__ == "__main__":
    _demo()
