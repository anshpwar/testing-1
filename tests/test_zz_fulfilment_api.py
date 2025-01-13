import json

from django.test import TestCase

from shopkit import rules


class ShipmentApiTests(TestCase):
    def post(self, url, body=None):
        return self.client.post(url, json.dumps(body or {}), content_type="application/json")

    def test_create_advance_and_read(self):
        created = self.post("/fulfilment/", {"order_ref": "SF-9", "destination_km": 300, "express": True})
        self.assertEqual(created.status_code, 201)
        pk = created.json()["id"]
        self.assertEqual(created.json()["surcharge_cents"], rules.express_surcharge_cents(300))
        self.assertEqual(self.post(f"/fulfilment/{pk}/advance/", {"status": "packed"}).json()["status"], "packed")
        self.assertEqual(self.client.get(f"/fulfilment/{pk}/").json()["timeline"][-1][0], "packed")

    def test_invalid_transition_is_409(self):
        pk = self.post("/fulfilment/", {"order_ref": "SF-10"}).json()["id"]
        self.assertEqual(self.post(f"/fulfilment/{pk}/advance/", {"status": "delivered"}).status_code, 409)

    def test_validation_and_missing(self):
        self.assertEqual(self.post("/fulfilment/", {}).status_code, 400)
        self.assertEqual(self.client.get("/fulfilment/999/").status_code, 404)
