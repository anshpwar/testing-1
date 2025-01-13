from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=24, unique=True)
    name = models.CharField(max_length=160)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price_cents = models.PositiveIntegerField()
    weight_g = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["sku"]

    def __str__(self):
        return f"{self.sku} {self.name}"

    def display_price(self):
        dollars, cents = divmod(self.price_cents, 100)
        return f"${dollars}.{cents:02d}"
