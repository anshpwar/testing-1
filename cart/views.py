import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from catalog.models import Product

from . import services
from .models import Cart


def _body(request):
    try:
        return json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return None


@csrf_exempt
@require_POST
def create(request):
    return JsonResponse({"token": services.new_cart().token}, status=201)


@csrf_exempt
@require_POST
def add(request, token):
    body = _body(request)
    if not body or not isinstance(body.get("qty"), int) or body["qty"] <= 0 or "sku" not in body:
        return JsonResponse({"error": "bad_request"}, status=400)
    try:
        cart = Cart.objects.get(token=token)
        services.add_item(cart, body["sku"], body["qty"])
    except Cart.DoesNotExist:
        return JsonResponse({"error": "cart_not_found"}, status=404)
    except Product.DoesNotExist:
        return JsonResponse({"error": "product_not_found"}, status=404)
    return JsonResponse({"items": cart.items.count()}, status=201)


@csrf_exempt
@require_POST
def coupon(request, token):
    body = _body(request) or {}
    try:
        cart = Cart.objects.get(token=token)
    except Cart.DoesNotExist:
        return JsonResponse({"error": "cart_not_found"}, status=404)
    cart.coupon_code = str(body.get("code", ""))[:32]
    cart.save(update_fields=["coupon_code"])
    return JsonResponse({"coupon": cart.coupon_code})


@require_GET
def quote(request, token):
    try:
        cart = Cart.objects.get(token=token)
    except Cart.DoesNotExist:
        return JsonResponse({"error": "cart_not_found"}, status=404)
    return JsonResponse({"currency": "USD", "quote": services.quote(cart)})
