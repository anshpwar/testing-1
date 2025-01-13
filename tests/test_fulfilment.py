from django.test import TestCase

from fulfilment import services
from shopkit import rules


class ShipmentLifecycleTests(TestCase):
    def test_happy_path_records_a_timeline(self):
        s = services.create_shipment("SF-1", 120)
        for status in ("packed", "shipped", "delivered"):
            services.advance(s, status)
        self.assertEqual([t[0] for t in services.timeline(s)], ["pending", "packed", "shipped", "delivered"])

    def test_invalid_transitions_are_rejected(self):
        s = services.create_shipment("SF-2", 10)
        with self.assertRaises(services.InvalidTransition):
            services.advance(s, "delivered")
        services.advance(s, "packed")
        with self.assertRaises(services.InvalidTransition):
            services.advance(s, "pending")

    def test_return_after_delivery_is_final(self):
        s = services.create_shipment("SF-3", 10)
        for status in ("packed", "shipped", "delivered", "returned"):
            services.advance(s, status)
        with self.assertRaises(services.InvalidTransition):
            services.advance(s, "shipped")

    def test_express_surcharge_follows_policy(self):
        express = services.create_shipment("SF-4", 400, express=True)
        standard = services.create_shipment("SF-5", 400)
        self.assertEqual(services.surcharge_cents(express), rules.express_surcharge_cents(400))
        self.assertEqual(services.surcharge_cents(standard), 0)
        self.assertEqual(express.carrier, "express")

    def test_return_deadline_uses_policy(self):
        self.assertEqual(services.return_deadline_days(15000), rules.return_window_days(15000))
