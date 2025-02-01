from django.http import JsonResponse

from .models import Order


def total(request, ref):
    obj = Order.objects.get(ref=ref)
    return JsonResponse({"total": obj.amount_cents * 2})
