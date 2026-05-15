"""
coin_change_base.py
-------------------------------------------------------------------------------
Universidad del Valle de Guatemala
Análisis y Diseño de Algoritmos - Sección 20 - Semestre 1, 2026
Proyecto 2 - Coin Change Problem (Interfaz común)

Integrantes:
    - Nicolás Concuá  (Carné No. 23197)
    - Esteban Cárcamo (Carné No. 23016)
    - Diego López     (Carné No. 23747)

Descripción:
    Clase base abstracta y utilidades compartidas entre las implementaciones
    DP y Greedy del Coin Change Problem.

    Centraliza las preocupaciones cruzadas (validación de entradas,
    encabezado/cierre verbose, CLI con argparse, runner de demo) para que
    coin_change_dp.py y coin_change_greedy.py se enfoquen exclusivamente
    en el algoritmo.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Tuple
import argparse


SEPARADOR_DOBLE = "═" * 52
SEPARADOR_SIMPLE = "─" * 52


Resultado = Tuple[Optional[int], List[int]]
SolverFn = Callable[..., Resultado]


class CoinChangeSolver(ABC):
    """Interfaz común para los resolvedores del Coin Change Problem.

    Patrón Template Method: `resolver` orquesta validación + encabezado
    verbose + algoritmo + cierre verbose. Las subclases solo implementan
    `_algoritmo`.
    """

    nombre: str = "CoinChange"

    @staticmethod
    def _validar_entradas(coins: List[int], W: int) -> None:
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

    def _imprimir_encabezado(self, coins: List[int], W: int) -> None:
        print(f"\n{SEPARADOR_DOBLE}")
        print(f"  {self.nombre}  coins={coins}  W={W}")
        print(f"{SEPARADOR_DOBLE}")

    @staticmethod
    def _imprimir_cierre() -> None:
        print(f"{SEPARADOR_DOBLE}\n")

    def resolver(self, coins: List[int], W: int, verbose: bool = False) -> Resultado:
        self._validar_entradas(coins, W)
        if verbose:
            self._imprimir_encabezado(coins, W)
        resultado = self._algoritmo(coins, W, verbose)
        if verbose:
            self._imprimir_cierre()
        return resultado

    @abstractmethod
    def _algoritmo(self, coins: List[int], W: int, verbose: bool) -> Resultado:
        """Implementación específica del algoritmo. Cada subclase la define."""
        ...


# ---------------------------------------------------------------------------
# Helpers de presentación (demo y CLI) compartidos por dp y greedy
# ---------------------------------------------------------------------------

def _formatear_resultado(coins: List[int], W: int, cantidad: Optional[int],
                        monedas: List[int], etiqueta_fallo: str,
                        mostrar_parcial: bool) -> str:
    if cantidad is None:
        if mostrar_parcial:
            return f"coins={coins}, W={W}  ->  {etiqueta_fallo}  (parcial: {monedas})"
        return f"coins={coins}, W={W}  ->  {etiqueta_fallo}"
    return f"coins={coins}, W={W}  ->  {cantidad} monedas  {monedas}"


def ejecutar_demo(
    solver_fn: SolverFn,
    casos: List[Tuple[List[int], int]],
    casos_verbose: List[Tuple[List[int], int]],
    etiqueta_fallo: str = "no representable",
    mostrar_parcial: bool = False,
) -> None:
    """Imprime una tabla resumen y luego el paso a paso de algunos casos."""
    print("=== Resumen rápido ===")
    for coins, W in casos:
        cantidad, monedas = solver_fn(coins, W)
        print(_formatear_resultado(coins, W, cantidad, monedas,
                                   etiqueta_fallo, mostrar_parcial))

    print("\n=== Paso a paso (verbose) ===")
    for coins, W in casos_verbose:
        solver_fn(coins, W, verbose=True)


def ejecutar_cli(
    descripcion: str,
    ejemplo: str,
    solver_fn: SolverFn,
    fn_demo: Callable[[], None],
    etiqueta_fallo: str = "no representable",
    mostrar_parcial: bool = False,
) -> None:
    """Procesa flags --coins, --W, --verbose; sin flags ejecuta `fn_demo`."""
    parser = argparse.ArgumentParser(description=descripcion, epilog=ejemplo)
    parser.add_argument("--coins", nargs="+", type=int, metavar="C",
                        help="Denominaciones (ej: --coins 1 3 4)")
    parser.add_argument("--W", type=int, help="Monto objetivo (ej: --W 6)")
    parser.add_argument("--verbose", action="store_true",
                        help="Mostrar el paso a paso del algoritmo")
    args = parser.parse_args()

    if args.coins and args.W is not None:
        cantidad, monedas = solver_fn(args.coins, args.W, verbose=args.verbose)
        if not args.verbose:
            print(_formatear_resultado(args.coins, args.W, cantidad, monedas,
                                       etiqueta_fallo, mostrar_parcial))
    else:
        fn_demo()
