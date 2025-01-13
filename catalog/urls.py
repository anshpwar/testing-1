from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="product-list"),
    path("json/", views.product_json, name="product-json"),
    path("category/<slug:slug>/", views.product_list, name="category-list"),
    path("<str:sku>/", views.product_detail, name="product-detail"),
]
