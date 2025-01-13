from django.db import models


class Shipment(models.Model):
    STATUSES = [
        ("pending", "Pending"),
        ("packed", "Packed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
    ]

    order_ref = models.CharField(max_length=24, db_index=True)
    carrier = models.CharField(max_length=32, default="standard")
    status = models.CharField(max_length=12, choices=STATUSES, default="pending")
    express = models.BooleanField(default=False)
    destination_km = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.order_ref} [{self.status}]"


class TrackingEvent(models.Model):
    shipment = models.ForeignKey(Shipment, on_delete=models.CASCADE, related_name="events")
    status = models.CharField(max_length=12)
    note = models.CharField(max_length=120, blank=True, default="")

    class Meta:
        ordering = ["id"]
