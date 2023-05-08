from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import item
from categories.models import Categories
from cart.views import _cart_id
from cart.models import ItemCart
from django.db.models import Q

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

def shop(request, categories_url = None):
    categories = None
    items = None

    if categories_url != None:
        category = get_object_or_404(Categories, url_category=categories_url)
        items = item.objects.filter(categories=category, availability=True)
        paginator = Paginator(items, 1)
        page = request.GET.get('page')
        items_on_page = paginator.get_page(page)
        how_many_items = items.count()
    else:
        items = item.objects.all().filter(availability=True).order_by('id')
        paginator = Paginator(items, 2)
        page = request.GET.get('page')
        items_on_page = paginator.get_page(page)
        how_many_items = items.count()

    seeHere = {
        'items': items_on_page,
        'how_many_items' : how_many_items
    }
    return render(request, 'shop/shop.html', seeHere)

#     if category_slug != None:
#         categories = get_object_or_404(Category, slug=category_slug)
#         products = Product.objects.filter(category=categories, is_available=True)
#         paginator = Paginator(products, 1)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#
#     else:
#         products = Product.objects.all().filter(is_available=True).order_by('id')
#         paginator = Paginator(products, 3)
#         page = request.GET.get('page')
#         paged_products = paginator.get_page(page)
#         product_count = products.count()
#
#     context = {
#         'products': paged_products,
#         'product_count': product_count,
#     }
#     return render(request, 'store/store.html', context)
#
#
def item_detail(request, categories_url, items_url):
    try:
        single_product = item.objects.get(categories__url_category=categories_url, url_item=items_url)
        in_cart = ItemCart.objects.filter(cart__id_cart=_cart_id(request), item=single_product).exists()
    except Exception as e:
        raise e
#
#     if request.user.is_authenticated:
#         try:
#             orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
#         except OrderProduct.DoesNotExist:
#             orderproduct = None
#     else:
#         orderproduct = None
#
#     # Get the reviews
#     reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
#
    context = {
        'single_product': single_product,
        'in_cart'       : in_cart,
        # 'orderproduct': orderproduct,
        # 'reviews': reviews,
    }
    return render(request, 'shop/item_detail.html', context)
#
#
def search(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = item.objects.order_by('-date_of_item_created').filter(Q(description_item__icontains=keyword) | Q(name_item__icontains=keyword))
            how_many_items = products.count()
    context = {
        'items': products,
        'how_many_items': how_many_items,
    }
    return render(request, 'shop/shop.html', context)
#
#
# def submit_review(request, product_id):
#     url = request.META.get('HTTP_REFERER')
#     if request.method == 'POST':
#         try:
#             reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
#             form = ReviewForm(request.POST, instance=reviews)
#             form.save()
#             messages.success(request, 'Thank you! Your review has been updated.')
#             return redirect(url)
#         except ReviewRating.DoesNotExist:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 data = ReviewRating()
#                 data.subject = form.cleaned_data['subject']
#                 data.rating = form.cleaned_data['rating']
#                 data.review = form.cleaned_data['review']
#                 data.ip = request.META.get('REMOTE_ADDR')
#                 data.product_id = product_id
#                 data.user_id = request.user.id
#                 data.save()
#                 messages.success(request, 'Thank you! Your review has been submitted.')
#                 return redirect(url)
