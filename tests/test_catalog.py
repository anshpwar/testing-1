from django.test import TestCase

from catalog.models import Category, Product


class ProductTests(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Lamps", slug="lamps")

    def test_display_price(self):
        p = Product.objects.create(sku="L-1", name="Desk lamp", category=self.cat, price_cents=1999)
        self.assertEqual(p.display_price(), "$19.99")
        p.price_cents = 5
        self.assertEqual(p.display_price(), "$0.05")

    def test_sku_is_unique(self):
        Product.objects.create(sku="L-2", name="A", category=self.cat, price_cents=1)
        with self.assertRaises(Exception):
            Product.objects.create(sku="L-2", name="B", category=self.cat, price_cents=2)

    def test_str(self):
        p = Product.objects.create(sku="L-3", name="Floor lamp", category=self.cat, price_cents=1)
        self.assertEqual(str(p), "L-3 Floor lamp")
