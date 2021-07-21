from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price','is_available','stocks','category','created_at','modified_date']
    prepopulated_fields= {'slug': ('product_name',)}

admin.site.register(Product,ProductAdmin)
