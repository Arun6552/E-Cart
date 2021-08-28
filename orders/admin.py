from django.contrib import admin
from .models import Payment,Order,OrderProdut
# Register your models here.


class OrderProdutInline(admin.TabularInline): 
    model = OrderProdut
    # readonly_fields = ['payment','user','product','quantity','product_price','is_ordered',]
    extra = 0
    
    
class OderAdmin(admin.ModelAdmin):
    list_display = ['order_number','full_name','phone','email','city','order_total','tax','status','ip','is_ordered']
    list_filter = ['status','is_ordered']
    search_fields = ['order_number','first_name','last_name','phone','email']
    list_per_page = 20
    inlines = [OrderProdutInline]
    

    
    
admin.site.register(Payment)
admin.site.register(Order,OderAdmin)
admin.site.register(OrderProdut)