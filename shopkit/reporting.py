"""Sales reporting over plain order dictionaries (no database access)."""
from collections import defaultdict

from . import rules


def sales_summary(orders):
    """Aggregate totals and loyalty points from an iterable of order dicts."""
    totals = defaultdict(int)
    for order in orders:
        totals["orders"] += 1
        totals["gross_cents"] += order["subtotal"]
        totals["discount_cents"] += order.get("bulk_discount", 0) + order.get("coupon_discount", 0)
        totals["shipping_cents"] += order.get("shipping", 0)
        totals["net_cents"] += order["total"]
        totals["loyalty_points"] += rules.loyalty_points(order["total"])
    return dict(totals)


def top_skus(lines, n=3):
    """Best-selling SKUs by units from (sku, qty) pairs; ties break alphabetically."""
    units = defaultdict(int)
    for sku, qty in lines:
        units[sku] += qty
    return sorted(units.items(), key=lambda kv: (-kv[1], kv[0]))[:n]


def reorder_list(daily_sales_by_sku, on_hand):
    """SKUs whose stock is at or below the policy reorder threshold."""
    out = []
    for sku, avg in sorted(daily_sales_by_sku.items()):
        if on_hand.get(sku, 0) <= rules.restock_threshold(avg):
            out.append(sku)
    return out
