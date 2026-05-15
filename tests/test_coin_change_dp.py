import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from coin_change_dp import coin_change_dp


class TestCoinChangeDP(unittest.TestCase):

    def test_canonico_usd_w30(self):
        """Sistema canónico USD: W=30 debe dar 2 monedas (25+5)."""
        cantidad, monedas = coin_change_dp([1, 5, 10, 25], 30)
        self.assertEqual(cantidad, 2)
        self.assertEqual(sum(monedas), 30)

    def test_canonico_usd_w87(self):
        """Sistema canónico USD: W=87 debe dar 5 monedas (25+25+25+10+2? no, 25*3+10+1+1=87). Verificar suma."""
        cantidad, monedas = coin_change_dp([1, 5, 10, 25], 87)
        self.assertIsNotNone(cantidad)
        self.assertEqual(sum(monedas), 87)
        # El óptimo conocido es 5 monedas: 25+25+25+10+1+1 no, sino 25*3+10+2? Con [1,5,10,25]:
        # 87 = 25*3 + 10 + 1*2 -> 6 monedas. Verificamos que la suma sea correcta y la cantidad mínima.
        # Con W=87: greedy da 3*25+10+1+1=6. DP también da 6 en este sistema canónico.
        self.assertEqual(cantidad, 6)

    def test_contraejemplo_greedy_clasico(self):
        """[1,3,4], W=6: DP debe dar 2 monedas (3+3)."""
        cantidad, monedas = coin_change_dp([1, 3, 4], 6)
        self.assertEqual(cantidad, 2)
        self.assertEqual(sum(monedas), 6)

    def test_no_representable(self):
        """[2,4,6], W=7: no representable, debe devolver (None, [])."""
        cantidad, monedas = coin_change_dp([2, 4, 6], 7)
        self.assertIsNone(cantidad)
        self.assertEqual(monedas, [])

    def test_w_cero(self):
        """W=0 siempre debe devolver (0, [])."""
        cantidad, monedas = coin_change_dp([1, 5, 10, 25], 0)
        self.assertEqual(cantidad, 0)
        self.assertEqual(monedas, [])

    def test_suma_monedas_igual_w(self):
        """Para todo caso representable, la suma de monedas reconstruidas debe ser W."""
        casos = [
            ([1, 5, 10, 25], 30),
            ([1, 3, 4],       6),
            ([1, 5, 10, 12, 25], 15),
            ([1, 7, 24, 42],  48),
        ]
        for coins, W in casos:
            cantidad, monedas = coin_change_dp(coins, W)
            self.assertIsNotNone(cantidad, msg=f"coins={coins}, W={W} no representable")
            self.assertEqual(sum(monedas), W,
                             msg=f"Suma incorrecta para coins={coins}, W={W}")

    def test_estabilidad_orden(self):
        """Denominaciones desordenadas deben dar el mismo resultado que ordenadas."""
        c1, m1 = coin_change_dp([1, 5, 10, 25], 30)
        c2, m2 = coin_change_dp([25, 1, 10, 5], 30)
        self.assertEqual(c1, c2)
        self.assertEqual(sum(m1), sum(m2))


if __name__ == "__main__":
    unittest.main()
