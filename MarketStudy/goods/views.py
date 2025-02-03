from multiprocessing import context
from django.shortcuts import render

from goods.models import Product


def catalog(request):

    goods = Product.objects.all()

    context = {
        'title': 'Каталог товарів',
        'content': 'Каталог товарів',
        'product': goods
    } 

    return render(request, 'goods/catalog.html', context);


def product(request, product_slug):

    product = Product.objects.get(slug=product_slug)
    context = {
        'title': product.name,  
        'product': product
    }
    return render(request, 'goods/product.html', context);