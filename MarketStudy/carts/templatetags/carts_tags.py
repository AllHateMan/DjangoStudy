from django import template

from carts.models import Cart

register = template.Library()

@register.simple_tag()
def users_carts(request):
    """Повертає кошик користувача"""
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user)