from django.contrib import admin
from .models import Product,Variation,ReviewRating
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_name','price','is_available','stocks','category','created_at','modified_date']
    prepopulated_fields= {'slug': ('product_name',)}
class VariationAdmin(admin.ModelAdmin):
    list_display = ['product','variation_category','variation_value','is_active',]
    list_editable = ('is_active',)
    list_filter = ['product','variation_category','variation_value','is_active',]

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)