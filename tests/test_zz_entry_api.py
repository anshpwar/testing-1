import json

from django.test import TestCase

from orders.models import Order


class OrderApiTests(TestCase):
    def test_summary_endpoint(self):
        Order.objects.create(ref="SF-200", amount_cents=1999, status="paid")
        resp = self.client.get("/entries/SF-200/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), {"ref": "SF-200", "amount_cents": 1999, "status": "paid"})

    def test_unknown_ref_is_404(self):
        self.assertEqual(self.client.get("/entries/nope/").status_code, 404)
