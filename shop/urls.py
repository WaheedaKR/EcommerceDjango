from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug:categories_url>/', views.shop, name='items_by_categories'),
    path('category/<slug:categories_url>/<slug:items_url>/', views.item_detail, name='item_detail'),
    path('search/', views.search, name='search'),
    # path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
