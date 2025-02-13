from django.http import JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from carts.utils import get_user_carts
from carts.models import Cart
from goods.models import Product

# Create your views here.
def cart_add(request):
    
    product_id = request.POST.get("product_id")
    
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)
        
        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1 
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)
            
        user_cart = get_user_carts(request)
    
    cart_items_html = render_to_string(
        "includes/includet_cart.html", {'carts': user_cart}, request=request)
    
    response_data = {
        "message": "Товар додано до кошика",
        "cart_items_html": cart_items_html,
    }
    
    return JsonResponse(response_data)

def cart_change(request):
    cart_id = request.POST.get("cart_id")
    cart = Cart.objects.get(id=cart_id)
    
    quantity = request.POST.get("quantity")
    cart.quantity = quantity
    cart.save()
    
    user_cart = get_user_carts(request)
    
    cart_items_html = render_to_string(
        "includes/includet_cart.html",
        {'carts': user_cart},
        request=request
    )
    
    response_data = {
        "message": "Кількість товару змінено",
        "cart_items_html": cart_items_html,
        "quantity": quantity,
        "total_quantity": user_cart.total_quantity(),
    }
    
    return JsonResponse(response_data)

def cart_remove(request):
    cart_id = request.POST.get("cart_id")
    
    cart = Cart.objects.get(id=cart_id)
    quantity_deleted = cart.quantity
    cart.delete()
    
    user_cart = get_user_carts(request)
    
    cart_items_html = render_to_string(
        "includes/includet_cart.html", 
        {'carts': user_cart}, 
        request=request
    )
    
    response_data = {
        "message": "Товар видалено з кошика",
        "cart_items_html": cart_items_html,
        "quantity_deleted": quantity_deleted,
        "total_quantity": user_cart.total_quantity(),
    }
    
    return JsonResponse(response_data)