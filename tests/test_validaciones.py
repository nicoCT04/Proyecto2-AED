import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import unittest
from coin_change_dp import coin_change_dp
from coin_change_greedy import coin_change_greedy


class TestValidacionesDP(unittest.TestCase):

    def test_w_negativo(self):
        with self.assertRaises(ValueError):
            coin_change_dp([1, 5, 10], -1)

    def test_w_string(self):
        with self.assertRaises(TypeError):
            coin_change_dp([1, 5, 10], "5")

    def test_coins_vacio(self):
        with self.assertRaises(ValueError):
            coin_change_dp([], 10)

    def test_coins_con_cero(self):
        with self.assertRaises(ValueError):
            coin_change_dp([1, 0, 5], 10)

    def test_coins_con_float(self):
        with self.assertRaises(TypeError):
            coin_change_dp([1, 2.5, 5], 10)

    def test_coins_no_es_lista(self):
        with self.assertRaises(TypeError):
            coin_change_dp("abc", 10)


class TestValidacionesGreedy(unittest.TestCase):

    def test_w_negativo(self):
        with self.assertRaises(ValueError):
            coin_change_greedy([1, 5, 10], -1)

    def test_w_string(self):
        with self.assertRaises(TypeError):
            coin_change_greedy([1, 5, 10], "5")

    def test_coins_vacio(self):
        with self.assertRaises(ValueError):
            coin_change_greedy([], 10)

    def test_coins_con_cero(self):
        with self.assertRaises(ValueError):
            coin_change_greedy([1, 0, 5], 10)

    def test_coins_con_float(self):
        with self.assertRaises(TypeError):
            coin_change_greedy([1, 2.5, 5], 10)

    def test_coins_no_es_lista(self):
        with self.assertRaises(TypeError):
            coin_change_greedy("abc", 10)


if __name__ == "__main__":
    unittest.main()
