from django.test import TestCase

from promotions.models import Coupon
from promotions.services import coupon_discount_cents
from shopkit import rules


class CouponTests(TestCase):
    def test_unknown_or_blank_code_gives_nothing(self):
        self.assertEqual(coupon_discount_cents("", 5000), 0)
        self.assertEqual(coupon_discount_cents("NOPE", 5000), 0)

    def test_inactive_coupon_ignored(self):
        Coupon.objects.create(code="OLD", percent_bp=2000, active=False)
        self.assertEqual(coupon_discount_cents("OLD", 5000), 0)

    def test_discount_is_capped_by_policy(self):
        Coupon.objects.create(code="HALF", percent_bp=5000)
        spend = 90000
        self.assertEqual(coupon_discount_cents("HALF", spend), min(spend // 2, rules.coupon_cap_cents(spend)))

    def test_no_discount_on_empty_spend(self):
        Coupon.objects.create(code="ANY", percent_bp=1000)
        self.assertEqual(coupon_discount_cents("ANY", 0), 0)
