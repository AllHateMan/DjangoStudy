
from django.shortcuts import get_list_or_404, render
from django.core.paginator import Paginator


from goods.utils import q_search
from goods.models import Product


def catalog(request, category_slug=None):

    page = request.GET.get('page', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        product = Product.objects.all()
    elif query:
        product = q_search(query)
        
    else :
        product = get_list_or_404 (Product.objects.filter(category__slug=category_slug))

    if on_sale:
        product = product.filter(discount__gt=0)

    if order_by and order_by != 'default':
        product = product.order_by(order_by)
    
    paginator = Paginator(product, 10)
    current_page = paginator.page(int(page))

    context = {
        'title': 'Каталог товарів',
        'content': 'Каталог товарів',
        'product': current_page,
        'slug_url': category_slug
    } 

    return render(request, 'goods/catalog.html', context)


def product(request, product_slug):

    product = Product.objects.get(slug=product_slug)
    context = {
        'title': product.name,  
        'product': product
    }
    return render(request, 'goods/product.html', context);