from django.http import Http404, JsonResponse

from .models import Order


def summary(request, ref):
    try:
        obj = Order.objects.get(ref=ref)
    except Order.DoesNotExist:
        raise Http404
    return JsonResponse({"ref": obj.ref, "amount_cents": obj.amount, "status": obj.status})
