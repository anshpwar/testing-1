import unittest

from shopkit import reporting, rules


class ReportingTests(unittest.TestCase):
    ORDERS = [
        {"subtotal": 10000, "bulk_discount": 500, "coupon_discount": 0, "shipping": 599, "total": 10099},
        {"subtotal": 2500, "shipping": 399, "total": 2899},
    ]

    def test_sales_summary_adds_up(self):
        s = reporting.sales_summary(self.ORDERS)
        self.assertEqual(s["orders"], 2)
        self.assertEqual(s["gross_cents"], 12500)
        self.assertEqual(s["discount_cents"], 500)
        self.assertEqual(s["net_cents"], 12998)
        self.assertEqual(s["loyalty_points"], rules.loyalty_points(10099) + rules.loyalty_points(2899))

    def test_empty_input(self):
        self.assertEqual(reporting.sales_summary([]), {})

    def test_top_skus_orders_by_units_then_name(self):
        lines = [("B", 2), ("A", 2), ("C", 5), ("A", 1)]
        self.assertEqual(reporting.top_skus(lines, 2), [("C", 5), ("A", 3)])

    def test_reorder_list_uses_threshold_policy(self):
        low = {"X": 3, "Y": 50}
        on_hand = {"X": rules.restock_threshold(3), "Y": rules.restock_threshold(50) + 1}
        self.assertEqual(reporting.reorder_list(low, on_hand), ["X"])
