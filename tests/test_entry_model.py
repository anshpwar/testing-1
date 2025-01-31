from django.test import TestCase

from orders.models import Order


class OrderModelTests(TestCase):
    def test_defaults(self):
        obj = Order.objects.create(ref="SF-100", amount=500)
        self.assertEqual(obj.status, "open")
        self.assertEqual(str(obj), "SF-100")

    def test_ref_is_unique(self):
        Order.objects.create(ref="SF-101", amount=1)
        with self.assertRaises(Exception):
            Order.objects.create(ref="SF-101", amount=2)
