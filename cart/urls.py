from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name='cart'),
    path('item_to_cart/<int:product_id>/', views.item_to_cart, name='item_to_cart'),
    path('item_removed_from_cart/<int:product_id>', views.item_removed_from_cart, name='item_removed_from_cart'),
    path('item_fully_removed/<int:product_id>', views.item_fully_removed, name='item_fully_removed'),
    path('checkout/', views.checkout, name='checkout'),
]
