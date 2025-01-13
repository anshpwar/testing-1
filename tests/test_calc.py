import unittest

from shopkit import calc


class CalcTests(unittest.TestCase):
    def test_combined_charge(self):
        self.assertEqual(calc.combined_charge(0), 399)
        self.assertEqual(calc.combined_charge(1), 399)
        self.assertEqual(calc.combined_charge(500), 999)
        self.assertEqual(calc.combined_charge(501), 1199)
