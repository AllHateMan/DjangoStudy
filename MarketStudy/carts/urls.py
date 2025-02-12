from django.urls import path
from carts import views

app_name = "carts"

urlpatterns = [
    path('cart_detail<int:product_id>/', views.cart_detail, name='cart_detail'),
    path('cart_add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart_remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
]