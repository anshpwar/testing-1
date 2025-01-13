import unittest

from shopkit import contract


class ContractTests(unittest.TestCase):
    def test_build_summary(self):
        rec = contract.Record("SF-1", 1250, "open")
        self.assertEqual(
            contract.build_summary(rec),
            {"ref": "SF-1", "amount_cents": 1250, "status": "open", "currency": "USD"},
        )

    def test_describe(self):
        summary = {"ref": "SF-2", "status": "closed", "amount_cents": 99, "currency": "EUR"}
        self.assertEqual(contract.describe(summary), "SF-2 closed 99 EUR")
