from django.http import Http404, JsonResponse
from django.shortcuts import render

from .models import Category, Product


def product_list(request, slug=None):
    products = Product.objects.filter(active=True).select_related("category")
    category = None
    if slug:
        try:
            category = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            raise Http404("unknown category")
        products = products.filter(category=category)
    return render(request, "catalog/product_list.html", {"products": products, "category": category})


def product_detail(request, sku):
    try:
        product = Product.objects.select_related("category").get(sku=sku, active=True)
    except Product.DoesNotExist:
        raise Http404("unknown product")
    return render(request, "catalog/product_detail.html", {"product": product})


def product_json(request):
    rows = [
        {"sku": p.sku, "name": p.name, "price": p.display_price(), "category": p.category.slug}
        for p in Product.objects.filter(active=True).select_related("category")
    ]
    return JsonResponse({"products": rows})
