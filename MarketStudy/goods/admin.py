from django.contrib import admin
from goods.models import Categories, Product

#admin.site.register(Categories)
#admin.site.register(Product)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'price', 'discount', 'category')
    list_editable = ('price', 'discount')
    search_fields = ('name', 'description')
    list_per_page = 10
    list_max_show_all = 100
    list_filter = ('discount', 'category', 'quantity')
            
