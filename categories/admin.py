from django.contrib import admin
from .models import Categories

# Register your models here.

class AdminCat(admin.ModelAdmin):
    prepopulated_fields = {'url_category': ('main_category',)}
    list_display = ('main_category', 'url_category')

admin.site.register(Categories, AdminCat)
