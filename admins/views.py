from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
#
# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
#
from cart.views import _cart_id
from cart.models import Cart, ItemCart
import requests


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            contactNo = form.cleaned_data['contactNo']
            emailAddress = form.cleaned_data['emailAddress']
            password = form.cleaned_data['password']
            username = emailAddress.split("@")[0]
            user = Account.objects.create_normaluser(name=name, surname=surname, emailAddress=emailAddress, username=username, password=password)
            user.contactNo = contactNo
            user.save()

            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = emailAddress
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            # messages.success(request, 'Thank you for registering with us. We have sent you a verification email to your email address [rathan.kumar@gmail.com]. Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+emailAddress)
            # return redirect('register')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':
        emailAddress = request.POST['emailAddress']
        password = request.POST['password']
        user = auth.authenticate(emailAddress=emailAddress, password=password)
#
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = ItemCart.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = ItemCart.objects.filter(cart=cart)
                    product_variation = []
                    for itemm in cart_item:
                        variation = itemm.variations.all()
                        product_variation.append(list(variation))
                    #
                    # # Get the cart items from the user to access his product variations
                    cart_item = ItemCart.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for itemm in cart_item:
                        existing_variation = itemm.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(itemm.id)


                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            itemm = ItemCart.objects.get(id=item_id)
                            itemm.cart_quantity += 1
                            itemm.user = user
                            itemm.save()
                        else:
                            cart_item = ItemCart.objects.filter(cart=cart)
                    for itemm in cart_item:
                        itemm.user = user
                        itemm.save()
            except:
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
#             return redirect('dashboard')
#
# #             messages.success(request, 'You are now logged in.')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                # next=/cart/checkout/
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')
#
#
@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')
    # return render(request, 'accounts/logout.html')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')
#
#
@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
#
#
def forgotPassword(request):
    if request.method == 'POST':
        emailAddress = request.POST['emailAddress']
        if Account.objects.filter(emailAddress=emailAddress).exists():
            user = Account.objects.get(emailAddress__exact=emailAddress)

            # Reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = emailAddress
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')
#
#
def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')


def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')
