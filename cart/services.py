"""Cart arithmetic. All fee schedules come from shopkit.rules."""
import secrets

from catalog.models import Product
from promotions.services import coupon_discount_cents
from shopkit import rules

from .models import Cart, CartItem


def new_cart():
    return Cart.objects.create(token=secrets.token_hex(16))


def add_item(cart, sku, qty):
    product = Product.objects.get(sku=sku, active=True)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"qty": qty})
    if not created:
        item.qty += qty
        item.save(update_fields=["qty"])
    return item


def _lines(cart):
    return list(cart.items.select_related("product"))


def subtotal_cents(cart):
    return sum(i.product.price_cents * i.qty for i in _lines(cart))


def bulk_discount_cents(cart):
    total = 0
    for i in _lines(cart):
        total += i.product.price_cents * i.qty * rules.bulk_discount_bp(i.qty) // 10000
    return total


def shipping_cents(cart):
    lines = _lines(cart)
    if not lines:
        return 0
    return rules.shipping_fee_cents(sum(i.product.weight_g * i.qty for i in lines))


def handling_cents(cart):
    return rules.handling_fee_cents(sum(i.qty for i in _lines(cart)))


def quote(cart):
    subtotal = subtotal_cents(cart)
    bulk = bulk_discount_cents(cart)
    coupon = coupon_discount_cents(cart.coupon_code, subtotal - bulk)
    shipping = shipping_cents(cart)
    handling = handling_cents(cart) if shipping else 0
    total = subtotal - bulk - coupon + shipping + handling
    return {
        "subtotal": subtotal,
        "bulk_discount": bulk,
        "coupon_discount": coupon,
        "shipping": shipping,
        "handling": handling,
        "total": total,
        "loyalty_points": rules.loyalty_points(total),
    }
