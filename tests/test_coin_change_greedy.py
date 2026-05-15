import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from coin_change_dp import coin_change_dp
from coin_change_greedy import coin_change_greedy


class TestCoinChangeGreedy(unittest.TestCase):

    def test_canonico_usd_w30(self):
        """Sistema canónico USD: W=30, greedy debe dar 2 monedas (óptimo)."""
        cantidad, monedas = coin_change_greedy([1, 5, 10, 25], 30)
        self.assertEqual(cantidad, 2)
        self.assertEqual(sum(monedas), 30)

    def test_suboptimo_clasico(self):
        """[1,3,4], W=6: greedy da 3 (4+1+1), DP da 2. Verificar greedy > dp."""
        gr, _ = coin_change_greedy([1, 3, 4], 6)
        opt, _ = coin_change_dp([1, 3, 4], 6)
        self.assertEqual(gr, 3)
        self.assertEqual(opt, 2)
        self.assertGreater(gr, opt)

    def test_suboptimo_fuerte(self):
        """[1,7,24,42], W=48: greedy da 7, DP da 2. Ratio = 3.5."""
        gr, _ = coin_change_greedy([1, 7, 24, 42], 48)
        opt, _ = coin_change_dp([1, 7, 24, 42], 48)
        self.assertEqual(opt, 2)
        self.assertEqual(gr, 7)
        self.assertAlmostEqual(gr / opt, 3.5)

    def test_greedy_falla_no_representable(self):
        """[2,4,6], W=7: greedy no puede completar, debe devolver None en cantidad."""
        cantidad, _ = coin_change_greedy([2, 4, 6], 7)
        self.assertIsNone(cantidad)

    def test_w_cero(self):
        """W=0 debe devolver (0, [])."""
        cantidad, monedas = coin_change_greedy([1, 5, 10, 25], 0)
        self.assertEqual(cantidad, 0)
        self.assertEqual(monedas, [])


if __name__ == "__main__":
    unittest.main()
