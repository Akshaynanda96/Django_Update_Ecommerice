from django.contrib import admin
from cart.models import Carts



class CartAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'brand' , 'artical' , 'size', 'color', 'product'  ,'qty' , 'total')


admin.site.register(Carts, CartAdmin)