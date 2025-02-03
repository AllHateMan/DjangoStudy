from django import template

from goods.models import Categories

register = template.Library()

@register.simple_tag()
def category_list():
    return Categories.objects.all()   