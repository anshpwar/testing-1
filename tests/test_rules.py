import unittest

from shopkit import rules


class RuleTests(unittest.TestCase):
    def test_shipping_fee_cents(self):
        self.assertEqual(rules.shipping_fee_cents(0), 399)
        self.assertEqual(rules.shipping_fee_cents(1), 399)
        self.assertEqual(rules.shipping_fee_cents(500), 399)
        self.assertEqual(rules.shipping_fee_cents(501), 599)
        self.assertEqual(rules.shipping_fee_cents(2000), 599)
        self.assertEqual(rules.shipping_fee_cents(2001), 999)
        self.assertEqual(rules.shipping_fee_cents(10000), 999)
        self.assertEqual(rules.shipping_fee_cents(10001), 1499)

    def test_handling_fee_cents(self):
        self.assertEqual(rules.handling_fee_cents(0), 0)
        self.assertEqual(rules.handling_fee_cents(1), 0)
        self.assertEqual(rules.handling_fee_cents(2), 150)
        self.assertEqual(rules.handling_fee_cents(5), 150)
        self.assertEqual(rules.handling_fee_cents(6), 300)
        self.assertEqual(rules.handling_fee_cents(20), 300)
        self.assertEqual(rules.handling_fee_cents(21), 600)

    def test_loyalty_points(self):
        self.assertEqual(rules.loyalty_points(0), 0)
        self.assertEqual(rules.loyalty_points(1), 0)
        self.assertEqual(rules.loyalty_points(999), 0)
        self.assertEqual(rules.loyalty_points(1000), 0)
        self.assertEqual(rules.loyalty_points(4999), 10)
        self.assertEqual(rules.loyalty_points(5000), 10)
        self.assertEqual(rules.loyalty_points(19999), 60)
        self.assertEqual(rules.loyalty_points(20000), 60)

    def test_bulk_discount_bp(self):
        self.assertEqual(rules.bulk_discount_bp(0), 0)
        self.assertEqual(rules.bulk_discount_bp(1), 0)
        self.assertEqual(rules.bulk_discount_bp(9), 0)
        self.assertEqual(rules.bulk_discount_bp(10), 300)
        self.assertEqual(rules.bulk_discount_bp(24), 300)
        self.assertEqual(rules.bulk_discount_bp(25), 600)
        self.assertEqual(rules.bulk_discount_bp(99), 600)
        self.assertEqual(rules.bulk_discount_bp(100), 1000)

    def test_return_window_days(self):
        self.assertEqual(rules.return_window_days(0), 14)
        self.assertEqual(rules.return_window_days(1), 14)
        self.assertEqual(rules.return_window_days(2000), 14)
        self.assertEqual(rules.return_window_days(2001), 30)
        self.assertEqual(rules.return_window_days(20000), 30)
        self.assertEqual(rules.return_window_days(20001), 45)
        self.assertEqual(rules.return_window_days(100000), 45)
        self.assertEqual(rules.return_window_days(100001), 60)

    def test_gift_wrap_cents(self):
        self.assertEqual(rules.gift_wrap_cents(0), 299)
        self.assertEqual(rules.gift_wrap_cents(1), 299)
        self.assertEqual(rules.gift_wrap_cents(2), 499)
        self.assertEqual(rules.gift_wrap_cents(3), 499)
        self.assertEqual(rules.gift_wrap_cents(4), 899)
        self.assertEqual(rules.gift_wrap_cents(10), 899)
        self.assertEqual(rules.gift_wrap_cents(11), 1499)

    def test_restock_threshold(self):
        self.assertEqual(rules.restock_threshold(0), 10)
        self.assertEqual(rules.restock_threshold(1), 10)
        self.assertEqual(rules.restock_threshold(5), 10)
        self.assertEqual(rules.restock_threshold(6), 40)
        self.assertEqual(rules.restock_threshold(25), 40)
        self.assertEqual(rules.restock_threshold(26), 150)
        self.assertEqual(rules.restock_threshold(100), 150)
        self.assertEqual(rules.restock_threshold(101), 400)

    def test_review_hold_hours(self):
        self.assertEqual(rules.review_hold_hours(0), 48)
        self.assertEqual(rules.review_hold_hours(1), 48)
        self.assertEqual(rules.review_hold_hours(7), 48)
        self.assertEqual(rules.review_hold_hours(8), 24)
        self.assertEqual(rules.review_hold_hours(30), 24)
        self.assertEqual(rules.review_hold_hours(31), 6)
        self.assertEqual(rules.review_hold_hours(180), 6)
        self.assertEqual(rules.review_hold_hours(181), 0)

    def test_fraud_review_score(self):
        self.assertEqual(rules.fraud_review_score(0), 1)
        self.assertEqual(rules.fraud_review_score(1), 1)
        self.assertEqual(rules.fraud_review_score(5000), 1)
        self.assertEqual(rules.fraud_review_score(5001), 3)
        self.assertEqual(rules.fraud_review_score(25000), 3)
        self.assertEqual(rules.fraud_review_score(25001), 7)
        self.assertEqual(rules.fraud_review_score(100000), 7)
        self.assertEqual(rules.fraud_review_score(100001), 15)

    def test_warranty_months(self):
        self.assertEqual(rules.warranty_months(0), 12)
        self.assertEqual(rules.warranty_months(1), 12)
        self.assertEqual(rules.warranty_months(5000), 12)
        self.assertEqual(rules.warranty_months(5001), 24)
        self.assertEqual(rules.warranty_months(30000), 24)
        self.assertEqual(rules.warranty_months(30001), 36)
        self.assertEqual(rules.warranty_months(150000), 36)
        self.assertEqual(rules.warranty_months(150001), 60)

    def test_price_rounding_step(self):
        self.assertEqual(rules.price_rounding_step(0), 1)
        self.assertEqual(rules.price_rounding_step(1), 1)
        self.assertEqual(rules.price_rounding_step(999), 1)
        self.assertEqual(rules.price_rounding_step(1000), 5)
        self.assertEqual(rules.price_rounding_step(9999), 5)
        self.assertEqual(rules.price_rounding_step(10000), 50)
        self.assertEqual(rules.price_rounding_step(99999), 50)
        self.assertEqual(rules.price_rounding_step(100000), 100)

    def test_cart_expiry_minutes(self):
        self.assertEqual(rules.cart_expiry_minutes(0), 30)
        self.assertEqual(rules.cart_expiry_minutes(1), 30)
        self.assertEqual(rules.cart_expiry_minutes(2), 90)
        self.assertEqual(rules.cart_expiry_minutes(5), 90)
        self.assertEqual(rules.cart_expiry_minutes(6), 240)
        self.assertEqual(rules.cart_expiry_minutes(20), 240)
        self.assertEqual(rules.cart_expiry_minutes(21), 1440)

    def test_coupon_cap_cents(self):
        self.assertEqual(rules.coupon_cap_cents(0), 500)
        self.assertEqual(rules.coupon_cap_cents(1), 500)
        self.assertEqual(rules.coupon_cap_cents(5000), 500)
        self.assertEqual(rules.coupon_cap_cents(5001), 2500)
        self.assertEqual(rules.coupon_cap_cents(20000), 2500)
        self.assertEqual(rules.coupon_cap_cents(20001), 10000)
        self.assertEqual(rules.coupon_cap_cents(100000), 10000)
        self.assertEqual(rules.coupon_cap_cents(100001), 20000)

    def test_tax_exempt_limit_cents(self):
        self.assertEqual(rules.tax_exempt_limit_cents(0), 0)
        self.assertEqual(rules.tax_exempt_limit_cents(1), 0)
        self.assertEqual(rules.tax_exempt_limit_cents(100000), 0)
        self.assertEqual(rules.tax_exempt_limit_cents(100001), 5000)
        self.assertEqual(rules.tax_exempt_limit_cents(500000), 5000)
        self.assertEqual(rules.tax_exempt_limit_cents(500001), 25000)
        self.assertEqual(rules.tax_exempt_limit_cents(2000000), 25000)
        self.assertEqual(rules.tax_exempt_limit_cents(2000001), 60000)

    def test_express_surcharge_cents(self):
        self.assertEqual(rules.express_surcharge_cents(0), 499)
        self.assertEqual(rules.express_surcharge_cents(1), 499)
        self.assertEqual(rules.express_surcharge_cents(50), 499)
        self.assertEqual(rules.express_surcharge_cents(51), 999)
        self.assertEqual(rules.express_surcharge_cents(300), 999)
        self.assertEqual(rules.express_surcharge_cents(301), 1999)
        self.assertEqual(rules.express_surcharge_cents(1500), 1999)
        self.assertEqual(rules.express_surcharge_cents(1501), 3999)

    def test_payment_retry_delay_s(self):
        self.assertEqual(rules.payment_retry_delay_s(0), 30)
        self.assertEqual(rules.payment_retry_delay_s(1), 30)
        self.assertEqual(rules.payment_retry_delay_s(2), 300)
        self.assertEqual(rules.payment_retry_delay_s(3), 300)
        self.assertEqual(rules.payment_retry_delay_s(4), 1800)
        self.assertEqual(rules.payment_retry_delay_s(6), 1800)
        self.assertEqual(rules.payment_retry_delay_s(7), 7200)
