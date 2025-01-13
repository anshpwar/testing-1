from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=32, unique=True)
    percent_bp = models.PositiveIntegerField(help_text="discount in basis points")
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
