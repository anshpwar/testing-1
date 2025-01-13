import json

from django.test import TestCase

from catalog.models import Category, Product
from promotions.models import Coupon
from shopkit import rules


class CartApiTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="Kitchen", slug="kitchen")
        Product.objects.create(sku="K-1", name="Kettle", category=cat, price_cents=4000, weight_g=1500)

    def post(self, url, body=None):
        return self.client.post(url, json.dumps(body or {}), content_type="application/json")

    def test_quote_round_trip(self):
        token = self.post("/cart/").json()["token"]
        self.assertEqual(self.post(f"/cart/{token}/items/", {"sku": "K-1", "qty": 2}).status_code, 201)
        quote = self.client.get(f"/cart/{token}/quote/").json()["quote"]
        self.assertEqual(quote["subtotal"], 8000)
        self.assertEqual(quote["shipping"], rules.shipping_fee_cents(3000))

    def test_validation_errors(self):
        token = self.post("/cart/").json()["token"]
        self.assertEqual(self.post(f"/cart/{token}/items/", {"sku": "K-1", "qty": 0}).status_code, 400)
        self.assertEqual(self.post(f"/cart/{token}/items/", {"sku": "NOPE", "qty": 1}).status_code, 404)
        self.assertEqual(self.client.get("/cart/missing/quote/").status_code, 404)

    def test_coupon_flow(self):
        Coupon.objects.create(code="SAVE10", percent_bp=1000)
        token = self.post("/cart/").json()["token"]
        self.post(f"/cart/{token}/items/", {"sku": "K-1", "qty": 1})
        self.assertEqual(self.post(f"/cart/{token}/coupon/", {"code": "SAVE10"}).json()["coupon"], "SAVE10")
        self.assertGreater(self.client.get(f"/cart/{token}/quote/").json()["quote"]["coupon_discount"], 0)
