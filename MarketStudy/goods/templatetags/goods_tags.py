from urllib.parse import urlencode
from django import template

from goods.models import Categories

register = template.Library()

@register.simple_tag()
def category_list():
    return Categories.objects.all() 

@register.simple_tag(takes_context=True)
def change_params(context, **kwards):
    querry = context['request'].GET.dict()
    querry.update(kwards)
    return urlencode(querry)