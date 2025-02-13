from django import template

from carts.utils import get_user_carts
from carts.models import Cart

register = template.Library()

@register.simple_tag()
def user_cart(request):
    return get_user_carts(request)