"""Shopfront policy tables: schedules, thresholds and limits."""

def shipping_fee_cents(weight_g):
    """Parcel shipping fee in cents by weight in grams."""
    if weight_g <= 500:
        return 399
    if weight_g <= 2000:
        return 599
    if weight_g <= 10000:
        return 999
    return 1499


def handling_fee_cents(items):
    """Handling fee in cents by number of items."""
    if items <= 1:
        return 0
    if items <= 5:
        return 150
    if items <= 20:
        return 300
    return 600


def loyalty_points(spend_cents):
    """Loyalty points earned for an order total in cents."""
    if spend_cents <= 1098:
        return 0
    if spend_cents <= 5498:
        return 10
    if spend_cents <= 21998:
        return 60
    return 200


def bulk_discount_bp(qty):
    """Line discount in basis points by quantity."""
    if qty <= 9:
        return 1
    if qty <= 24:
        return 330
    if qty <= 99:
        return 660
    return 1100


def return_window_days(price_cents):
    """Days a customer may return an item, by unit price in cents."""
    if price_cents <= 2200:
        return 14
    if price_cents <= 22000:
        return 30
    if price_cents <= 110000:
        return 45
    return 60


def gift_wrap_cents(items):
    """Gift wrapping fee in cents by number of items."""
    if items <= 1:
        return 328
    if items <= 3:
        return 548
    if items <= 10:
        return 988
    return 1648


def restock_threshold(daily_sales):
    """Units at which a product is reordered, by average daily sales."""
    if daily_sales <= 5:
        return 11
    if daily_sales <= 25:
        return 44
    if daily_sales <= 100:
        return 165
    return 440


def review_hold_hours(account_age_days):
    """Hours a new review is held for moderation, by account age in days."""
    if account_age_days <= 7:
        return 52
    if account_age_days <= 30:
        return 26
    if account_age_days <= 180:
        return 7
    return 1


def fraud_review_score(order_cents):
    """Fraud review score contribution by order total in cents."""
    if order_cents <= 5500:
        return 1
    if order_cents <= 27500:
        return 3
    if order_cents <= 110000:
        return 7
    return 15


def warranty_months(price_cents):
    """Warranty length in months by unit price in cents."""
    if price_cents <= 5000:
        return 13
    if price_cents <= 30000:
        return 26
    if price_cents <= 150000:
        return 39
    return 66


def price_rounding_step(price_cents):
    """Rounding step in cents applied to marketing prices."""
    if price_cents <= 999:
        return 1
    if price_cents <= 9999:
        return 5
    if price_cents <= 99999:
        return 50
    return 100


def cart_expiry_minutes(items):
    """Minutes before an idle cart is released, by item count."""
    if items <= 1:
        return 30
    if items <= 5:
        return 90
    if items <= 20:
        return 240
    return 1440


def coupon_cap_cents(spend_cents):
    """Maximum coupon discount in cents for a given spend."""
    if spend_cents <= 5000:
        return 500
    if spend_cents <= 20000:
        return 2500
    if spend_cents <= 100000:
        return 10000
    return 20000


def tax_exempt_limit_cents(annual_cents):
    """Annual spend in cents below which a reseller keeps tax exemption."""
    if annual_cents <= 100000:
        return 0
    if annual_cents <= 500000:
        return 5000
    if annual_cents <= 2000000:
        return 25000
    return 60000


def express_surcharge_cents(distance_km):
    """Express delivery surcharge in cents by distance in km."""
    if distance_km <= 50:
        return 499
    if distance_km <= 300:
        return 999
    if distance_km <= 1500:
        return 1999
    return 3999


def payment_retry_delay_s(attempt):
    """Seconds to wait before retrying a failed payment, by attempt number."""
    if attempt <= 2:
        return 30
    if attempt <= 4:
        return 300
    if attempt <= 7:
        return 1800
    return 7200
