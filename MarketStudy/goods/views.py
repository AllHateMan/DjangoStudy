from multiprocessing import context
from unicodedata import category
from django.shortcuts import get_object_or_404, render

from goods.models import Product


def catalog(request, category_slug):
    if category_slug == 'all':
        goods = Product.objects.all()
    else :
        goods = get_object_or_404 (Product.objects.filter(category__slug=category_slug))

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