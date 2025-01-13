from django.test import TestCase

from cart import services
from catalog.models import Category, Product
from promotions.models import Coupon
from shopkit import rules


class QuoteTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="Kitchen", slug="kitchen")
        self.kettle = Product.objects.create(sku="K-1", name="Kettle", category=cat, price_cents=4000, weight_g=1500)
        self.mug = Product.objects.create(sku="M-1", name="Mug", category=cat, price_cents=800, weight_g=300)
        self.cart = services.new_cart()

    def test_subtotal_and_item_merge(self):
        services.add_item(self.cart, "K-1", 1)
        services.add_item(self.cart, "M-1", 2)
        services.add_item(self.cart, "M-1", 1)
        self.assertEqual(services.subtotal_cents(self.cart), 4000 + 3 * 800)
        self.assertEqual(self.cart.items.count(), 2)

    def test_shipping_and_handling_follow_policy_tables(self):
        services.add_item(self.cart, "K-1", 1)
        services.add_item(self.cart, "M-1", 2)
        weight = 1500 + 2 * 300
        self.assertEqual(services.shipping_cents(self.cart), rules.shipping_fee_cents(weight))
        self.assertEqual(services.handling_cents(self.cart), rules.handling_fee_cents(3))

    def test_empty_cart_ships_nothing(self):
        q = services.quote(self.cart)
        self.assertEqual((q["shipping"], q["handling"], q["total"]), (0, 0, 0))

    def test_quote_total_is_consistent(self):
        services.add_item(self.cart, "K-1", 2)
        q = services.quote(self.cart)
        self.assertEqual(q["total"], q["subtotal"] - q["bulk_discount"] - q["coupon_discount"] + q["shipping"] + q["handling"])
        self.assertEqual(q["loyalty_points"], rules.loyalty_points(q["total"]))

    def test_coupon_is_applied_through_promotions(self):
        Coupon.objects.create(code="SAVE10", percent_bp=1000)
        self.cart.coupon_code = "SAVE10"
        self.cart.save()
        services.add_item(self.cart, "K-1", 1)
        q = services.quote(self.cart)
        self.assertEqual(q["coupon_discount"], min(4000 * 1000 // 10000, rules.coupon_cap_cents(4000)))
