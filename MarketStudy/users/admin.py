from django.contrib import admin
from orders.admin import OrderTabulareAdmin
from users.models import User
from carts.admin import CartTabInline

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_per_page = 10
    list_max_show_all = 100

    inlines = [CartTabInline, OrderTabulareAdmin]

