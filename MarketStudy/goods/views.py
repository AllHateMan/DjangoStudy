from multiprocessing import context
from django.shortcuts import render

from goods.models import Product


def catalog(request):

    producte = Product.objects.all()

    context = {
        'title': 'Каталог товарів',
        'content': 'Каталог товарів',
        'product': producte
    }

    return render(request, 'goods/catalog.html', context);


def product(request):
    return render(request, 'goods/product.html');