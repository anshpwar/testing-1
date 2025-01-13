from django.urls import path

from . import views

urlpatterns = [
    path("", views.create, name="cart-create"),
    path("<str:token>/items/", views.add, name="cart-add"),
    path("<str:token>/coupon/", views.coupon, name="cart-coupon"),
    path("<str:token>/quote/", views.quote, name="cart-quote"),
]
