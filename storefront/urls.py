from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("catalog/", include("catalog.urls")),
    path("cart/", include("cart.urls")),
    path("fulfilment/", include("fulfilment.urls")),
    path("entries/", include("orders.urls")),
]
