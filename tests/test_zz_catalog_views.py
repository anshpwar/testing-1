import json

from django.test import TestCase

from catalog.models import Category, Product


class CatalogViewTests(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="Lamps", slug="lamps")
        other = Category.objects.create(name="Mugs", slug="mugs")
        Product.objects.create(sku="L-1", name="Desk lamp", category=cat, price_cents=1999)
        Product.objects.create(sku="U-1", name="Blue mug", category=other, price_cents=800)
        Product.objects.create(sku="X-1", name="Retired lamp", category=cat, price_cents=100, active=False)

    def test_list_page_renders_active_products(self):
        resp = self.client.get("/catalog/")
        self.assertContains(resp, "Desk lamp")
        self.assertContains(resp, "$19.99")
        self.assertNotContains(resp, "Retired lamp")

    def test_category_filter(self):
        resp = self.client.get("/catalog/category/mugs/")
        self.assertContains(resp, "Blue mug")
        self.assertNotContains(resp, "Desk lamp")
        self.assertEqual(self.client.get("/catalog/category/none/").status_code, 404)

    def test_detail_page(self):
        resp = self.client.get("/catalog/L-1/")
        self.assertContains(resp, "Price: $19.99")
        self.assertEqual(self.client.get("/catalog/ZZ/").status_code, 404)

    def test_json_listing(self):
        data = json.loads(self.client.get("/catalog/json/").content)
        self.assertEqual([p["sku"] for p in data["products"]], ["L-1", "U-1"])
