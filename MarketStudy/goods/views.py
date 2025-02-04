from multiprocessing import context
from unicodedata import category
from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator

from goods.models import Product


def catalog(request, category_slug):

    page = request.GET.get('page', 1)

    if category_slug == 'all':
        product = Product.objects.all()
    else :
        product = get_list_or_404 (Product.objects.filter(category__slug=category_slug))
    
    paginator = Paginator(product, 3)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Каталог товарів',
        'content': 'Каталог товарів',
        'product': current_page,
        'slug_url': category_slug
    } 

    return render(request, 'goods/catalog.html', context);


def product(request, product_slug):

    product = Product.objects.get(slug=product_slug)
    context = {
        'title': product.name,  
        'product': product
    }
    return render(request, 'goods/product.html', context);