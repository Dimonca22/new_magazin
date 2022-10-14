from django.shortcuts import render
from django.views.generic.base import View
from .models import Product


class ProductView(View):
    """Список комплектов"""
    def get(self, request):
        product = Product.objects.all()
        return render(request, "product/shop.html", {'shop_list': product})
