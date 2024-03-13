from django.contrib import admin
from .models import Watch,Cart,Order,Customer
# Register your models here.
@admin.register(Watch)
class WatchAdmin(admin.ModelAdmin):
    list_display= ['id','name','small_description','description','selling_price','discounted_price']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display= ['id','user','product','quantity']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display= ['id','user','name','address','city','state','pincode']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display= ['id','user','customer','watch','quantity','order_at','status']

