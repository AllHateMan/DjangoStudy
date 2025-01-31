from django.contrib import admin
from goods.models import Categories, Product

#admin.site.register(Categories)
#admin.site.register(Product)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
