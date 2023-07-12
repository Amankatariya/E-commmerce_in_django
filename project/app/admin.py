from django.contrib import admin
from .models import *

# Register your models here.

class product_imgs(admin.TabularInline):
    model=product_img
    
class product_Admin(admin.ModelAdmin):
    inlines=[product_imgs]
    list_display= ('name','category')
    # prepopulated_fields = {"slug": ("product_name",)} 

class OrderItems(admin.TabularInline):
    model=OrderItem

class order_Admin(admin.ModelAdmin):
    inlines=[OrderItems]
    list_display=('first_name', 'email', 'amount', 'paid','razorpay_order_id', 'phone')


admin.site.register(product_img)
admin.site.register(Product,product_Admin)
admin.site.register(section)
admin.site.register(category)
admin.site.register(Order,order_Admin)
admin.site.register(OrderItem)


admin.site.register(slider)