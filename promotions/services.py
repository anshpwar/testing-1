from shopkit import rules

from .models import Coupon


def coupon_discount_cents(code, spend_cents):
    """Percentage coupon discount, capped by the policy cap for the spend level."""
    if not code or spend_cents <= 0:
        return 0
    try:
        coupon = Coupon.objects.get(code=code, active=True)
    except Coupon.DoesNotExist:
        return 0
    raw = spend_cents * coupon.percent_bp // 10000
    return min(raw, rules.coupon_cap_cents(spend_cents))
