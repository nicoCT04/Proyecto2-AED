import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from canonicity_check import es_canonico
from coin_change_dp import coin_change_dp
from coin_change_greedy import coin_change_greedy


class TestCanonicityCheck(unittest.TestCase):

    def test_usd_canonico(self):
        """Sistema USD [1,5,10,25] es canónico."""
        canonico, contra = es_canonico([1, 5, 10, 25])
        self.assertTrue(canonico)
        self.assertIsNone(contra)

    def test_eur_canonico(self):
        """Sistema EUR [1,2,5,10,20,50,100,200] es canónico."""
        canonico, contra = es_canonico([1, 2, 5, 10, 20, 50, 100, 200])
        self.assertTrue(canonico)
        self.assertIsNone(contra)

    def test_no_canonico_clasico(self):
        """Sistema [1,3,4] NO es canónico."""
        canonico, contra = es_canonico([1, 3, 4])
        self.assertFalse(canonico)
        self.assertIsNotNone(contra)

    def test_no_canonico_mixto(self):
        """Sistema [1,5,10,12,25] NO es canónico."""
        canonico, contra = es_canonico([1, 5, 10, 12, 25])
        self.assertFalse(canonico)
        self.assertIsNotNone(contra)

    def test_no_canonico_fuerte(self):
        """Sistema [1,7,24,42] NO es canónico."""
        canonico, contra = es_canonico([1, 7, 24, 42])
        self.assertFalse(canonico)
        self.assertIsNotNone(contra)

    def test_contraejemplo_verifica_diferencia(self):
        """Para cada contraejemplo reportado, verificar que DP y greedy efectivamente difieren."""
        sistemas_no_canonicos = [
            [1, 3, 4],
            [1, 5, 10, 12, 25],
            [1, 7, 24, 42],
        ]
        for coins in sistemas_no_canonicos:
            canonico, contra = es_canonico(coins)
            self.assertFalse(canonico, msg=f"Se esperaba no canónico para {coins}")
            self.assertIsNotNone(contra)
            opt, _ = coin_change_dp(coins, contra)
            gr, _ = coin_change_greedy(coins, contra)
            self.assertIsNotNone(opt)
            # greedy es None (fallo) o subóptimo
            self.assertTrue(gr is None or gr != opt,
                            msg=f"Contraejemplo W={contra} no muestra diferencia para {coins}")

    def test_dos_denominaciones_siempre_canonico(self):
        """Sistemas con solo 2 denominaciones (incluida la 1) son canónicos."""
        canonico, contra = es_canonico([1, 7])
        self.assertTrue(canonico)
        self.assertIsNone(contra)


if __name__ == "__main__":
    unittest.main()
