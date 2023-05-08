from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import item
from .models import Cart
from .models import ItemCart
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required



def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def item_to_cart(request, product_id):
    product = item.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(id_cart=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            id_cart = _cart_id(request)
        )
    cart.save()

    try:
        cart_item = ItemCart.objects.get(item=product, cart=cart)
        cart_item.cart_quantity += 1
        cart_item.save()
    except ItemCart.DoesNotExist:
        cart_item = ItemCart.objects.create(
            item = product,
            cart_quantity = 1,
            cart = cart,
        )
        cart_item.save()

    return redirect('cart')

def item_removed_from_cart(request, product_id):

    product = get_object_or_404(item, id=product_id)
    cart = Cart.objects.get(id_cart=_cart_id(request))
    cart_item = ItemCart.objects.get(item=product, cart=cart)
    if cart_item.cart_quantity > 1:
            cart_item.cart_quantity -= 1
            cart_item.save()
    else:
        cart_item.delete()
    # except:
    #     pass
    return redirect('cart')


def item_fully_removed(request, product_id):
    product = get_object_or_404(item, id=product_id)
    cart = Cart.objects.get(id_cart=_cart_id(request))
    cart_item = ItemCart.objects.get(item=product, cart=cart)
    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        final_total = 0
        cart = Cart.objects.get(id_cart=_cart_id(request))
        cart_items = ItemCart.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.item.cost * cart_item.cart_quantity)
            quantity += cart_item.cart_quantity
        tax = (2 * total)/100
        final_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' :  total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'final_total' : final_total,
    }
    return render(request, 'shop/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        final_total = 0
        cart = Cart.objects.get(id_cart=_cart_id(request))
        cart_items = ItemCart.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.item.cost * cart_item.cart_quantity)
            quantity += cart_item.cart_quantity
        tax = (2 * total)/100
        final_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total' :  total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'final_total' : final_total,
    }
    return render(request, 'shop/checkout.html', context)

# @login_required(login_url='login')
# def checkout(request, total=0, quantity=0, cart_items=None):
#     try:
#         tax = 0
#         final_total = 0
#         if request.user.is_authenticated:
#             cart_items = ItemCart.objects.filter(user=request.user, is_active=True)
#         else:
#             cart = Cart.objects.get(id_cart=_cart_id(request))
#             cart_items = ItemCart.objects.filter(cart=cart, is_active=True)
#         for cart_item in cart_items:
#             total += (cart_item.item.cost * cart_item.cart_quantity)
#             quantity += cart_item.cart_quantity
#         tax = (2 * total)/100
#         final_total = total + tax
#     except ObjectDoesNotExist:
#         pass #just ignore
#
#     context = {
#         'total': total,
#         'quantity': quantity,
#         'cart_items': cart_items,
#         'tax'       : tax,
#         'final_total': final_total,
#     }
#     return render(request, 'shop/checkout.html', context)
