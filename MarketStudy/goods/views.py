from django.http import Http404
from django.views.generic import DetailView, ListView
from goods.models import Product
from goods.utils import q_search


class CatalogView(ListView):
    model = Product
    template_name = "goods/catalog.html"
    context_object_name = "product"
    paginate_by = 3
    allow_empty = False
    slug_url_kwarg = "category_slug"
    
    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")
        
        
        if category_slug == "all":
            product = super().get_queryset()
        else:
            product = super().get_queryset().filter(category__slug=category_slug)
            if not product.exists():
                raise Http404()
        if on_sale:
            product = product.filter(discount__gt=0)
        if order_by and order_by != "default":
            product = product.order_by(order_by)
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Каталог"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        return context

class ProductView(DetailView):
    template_name = "goods/product.html"
    slug_url_kwarg = "product_slug"
    context_object_name = "product"
    def get_object(self, queryset=None):
        product = Product.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

class SearchView(ListView):
    model = Product
    template_name = "goods/catalog.html"
    context_object_name = "product"
    paginate_by = 3
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        
        if query:
            product = q_search(query)
        else:
            product = Product.objects.all()
            
        if on_sale:
            product = product.filter(discount__gt=0)
        if order_by and order_by != "default":
            product = product.order_by(order_by)
        return product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пошук"
        return context
