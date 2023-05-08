from django.contrib import admin
from .models import item

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name_item', 'cost', 'stock_item', 'categories', 'date_of_item_created', 'availability')
    prepopulated_fields = {'url_item': ('name_item',)}

# class VariationAdmin(admin.ModelAdmin):
#     list_display = ('product', 'variation_category', 'variation_value', 'is_active')
#     list_editable = ('is_active',)
#     list_filter = ('product', 'variation_category', 'variation_value')

admin.site.register(item, ItemAdmin)
# admin.site.register(Variation, VariationAdmin)
# admin.site.register(ReviewRating)
