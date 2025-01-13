from django.urls import path

from . import views

urlpatterns = [
    path("", views.create, name="shipment-create"),
    path("<int:pk>/", views.detail, name="shipment-detail"),
    path("<int:pk>/advance/", views.advance, name="shipment-advance"),
]
