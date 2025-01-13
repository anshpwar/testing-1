from django.db import models

from catalog.models import Product


class Cart(models.Model):
    token = models.CharField(max_length=40, unique=True)
    coupon_code = models.CharField(max_length=32, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty = models.PositiveIntegerField()

    class Meta:
        unique_together = [("cart", "product")]
