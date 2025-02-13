from carts.models import Cart


def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).order_by('product__name')
    return []