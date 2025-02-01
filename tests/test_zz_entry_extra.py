from django.test import TestCase

from orders import api_extra
from orders.models import Order


class ExtraApiTests(TestCase):
    def test_total(self):
        Order.objects.create(ref="SF-300", amount_cents=5)
        resp = api_extra.total(None, "SF-300")
        self.assertEqual(resp.status_code, 200)
