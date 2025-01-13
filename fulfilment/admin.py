from django.contrib import admin

from .models import Shipment, TrackingEvent


class TrackingEventInline(admin.TabularInline):
    model = TrackingEvent
    extra = 0


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    inlines = [TrackingEventInline]
    list_display = ("order_ref", "carrier", "status", "express")
    list_filter = ("status", "express")
