from django.contrib import admin
from products.models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', )

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)