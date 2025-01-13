import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from . import services
from .models import Shipment


def _payload(shipment):
    return {
        "id": shipment.id,
        "order_ref": shipment.order_ref,
        "status": shipment.status,
        "surcharge_cents": services.surcharge_cents(shipment),
        "timeline": services.timeline(shipment),
    }


@csrf_exempt
@require_POST
def create(request):
    try:
        body = json.loads(request.body or b"{}")
        shipment = services.create_shipment(body["order_ref"], int(body.get("destination_km", 0)), bool(body.get("express")))
    except (KeyError, ValueError, TypeError):
        return JsonResponse({"error": "bad_request"}, status=400)
    return JsonResponse(_payload(shipment), status=201)


@csrf_exempt
@require_POST
def advance(request, pk):
    try:
        shipment = Shipment.objects.get(pk=pk)
    except Shipment.DoesNotExist:
        return JsonResponse({"error": "not_found"}, status=404)
    body = json.loads(request.body or b"{}")
    try:
        services.advance(shipment, body.get("status", ""), body.get("note", ""))
    except services.InvalidTransition as exc:
        return JsonResponse({"error": "invalid_transition", "detail": str(exc)}, status=409)
    return JsonResponse(_payload(shipment))


@require_GET
def detail(request, pk):
    try:
        return JsonResponse(_payload(Shipment.objects.get(pk=pk)))
    except Shipment.DoesNotExist:
        return JsonResponse({"error": "not_found"}, status=404)
