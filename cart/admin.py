from django.contrib import admin
from .models import Cart, ItemCart
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id_cart', 'date_of_cart_added')
#
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'cart', 'cart_quantity', 'is_active')

admin.site.register(Cart)
admin.site.register(ItemCart, CartItemAdmin)

