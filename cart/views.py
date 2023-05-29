from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import item, Variation
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
    current_user = request.user
    product = item.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == 'POST':
            if request.method == 'POST':
                for itemm in request.POST:
                    key = itemm
                    value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = ItemCart.objects.filter(item=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = ItemCart.objects.filter(item=product, user=current_user)
            ex_var_list = []
            id = []
            for itemm in cart_item:
                existing_variation = itemm.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(itemm.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                itemm = ItemCart.objects.get(item=product, id=item_id)
                itemm.cart_quantity += 1
                itemm.save()
            else:
                itemm = ItemCart.objects.create(item=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    itemm.variations.clear()
                    itemm.variations.add(*product_variation)
                itemm.save()
        else:
            cart_item = ItemCart.objects.create(
                item=product,
                cart_quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

    else:
        product_variation = []
        if request.method == 'POST':
            if request.method == 'POST':
                for itemm in request.POST:
                    key = itemm
                    value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                      variation_value__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(id_cart=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                id_cart=_cart_id(request)
            )
        cart.save()

        is_cart_item_exists = ItemCart.objects.filter(item=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = ItemCart.objects.filter(item=product, cart=cart)
            ex_var_list = []
            id = []
            for itemm in cart_item:
                existing_variation = itemm.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(itemm.id)

            if product_variation in ex_var_list:
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                itemm = ItemCart.objects.get(item=product, id=item_id)
                itemm.cart_quantity += 1
                itemm.save()
            else:
                itemm = ItemCart.objects.create(item=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    itemm.variations.clear()
                    itemm.variations.add(*product_variation)
                itemm.save()
        else:
            cart_item = ItemCart.objects.create(
                item=product,
                cart_quantity=1,
                cart=cart,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

def item_removed_from_cart(request, product_id, cart_item_id):
    # cart = Cart.objects.get(id_cart=_cart_id(request))
    product = get_object_or_404(item, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = ItemCart.objects.get(item=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(id_cart=_cart_id(request))
            cart_item = ItemCart.objects.get(item=product, cart=cart, id=cart_item_id)
        if cart_item.cart_quantity > 1:
            cart_item.cart_quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')


def item_fully_removed(request, product_id, cart_item_id):
    product = get_object_or_404(item, id=product_id)
    if request.user.is_authenticated:
        cart_item = ItemCart.objects.get(item=product, user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(id_cart=_cart_id(request))
    # product = get_object_or_404(item, id=product_id)
        cart_item = ItemCart.objects.get(item=product, cart=cart, id = cart_item_id)
    cart_item.delete()

    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        final_total = 0
        if request.user.is_authenticated:
            cart_items = ItemCart.objects.filter(user=request.user, is_active=True)
        else:
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
        if request.user.is_authenticated:
            cart_items = ItemCart.objects.filter(user=request.user, is_active=True)
        else:
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
