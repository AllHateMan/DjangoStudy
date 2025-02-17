from django.contrib import admin
from carts.models import Cart


class CartTabInline(admin.TabularInline):
    model = Cart
    fields = ('product', 'quantity')
    search_fields = ('product__name', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 1

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user_display', 'product__name', 'quantity', 'created_timestamp')
    list_filter = ('user', 'product__name')
    search_fields = ('user__username', 'product__name')
    list_per_page = 10
    list_max_show_all = 100

    def user_display(self, obj):
        if obj.user:
            return str(obj.user)
        return 'Анонімний користувач'

