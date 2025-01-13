"""Shipment lifecycle. Surcharges and return windows come from the shopkit policy tables."""
from shopkit import rules

from .models import Shipment, TrackingEvent

TRANSITIONS = {
    "pending": {"packed"},
    "packed": {"shipped"},
    "shipped": {"delivered", "returned"},
    "delivered": {"returned"},
    "returned": set(),
}


class InvalidTransition(Exception):
    pass


def create_shipment(order_ref, destination_km, express=False, carrier="standard"):
    shipment = Shipment.objects.create(order_ref=order_ref, destination_km=destination_km, express=express,
                                       carrier="express" if express else carrier)
    TrackingEvent.objects.create(shipment=shipment, status="pending", note="shipment created")
    return shipment


def advance(shipment, new_status, note=""):
    if new_status not in TRANSITIONS[shipment.status]:
        raise InvalidTransition(f"{shipment.status} -> {new_status}")
    shipment.status = new_status
    shipment.save(update_fields=["status"])
    TrackingEvent.objects.create(shipment=shipment, status=new_status, note=note)
    return shipment


def surcharge_cents(shipment):
    return rules.express_surcharge_cents(shipment.destination_km) if shipment.express else 0


def return_deadline_days(unit_price_cents):
    return rules.return_window_days(unit_price_cents)


def timeline(shipment):
    return [(e.status, e.note) for e in shipment.events.all()]
