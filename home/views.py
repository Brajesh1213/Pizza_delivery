from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(
    api_key=settings.API_KEY,
    auth_token=settings.AUTH_TOKEN,
    endpoint="https://test.instamojo.com/api/1.1/",
)

def home(request):
    pizzas = Pizza.objects.all()
    context = {'pizzas': pizzas}
    return render(request, 'home.html', context)

def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user_obj = User.objects.filter(username=username)

            if not user_obj.exists():
                messages.warning(request, 'Username does not exist')
                return redirect('/login/')
            user_obj = authenticate(request, username=username, password=password)

            if user_obj:
                login(request, user_obj)

                messages.success(request, "Account logged in")
                return redirect('/')
            else:
                messages.error(request, 'Wrong Password')

        except Exception as e:
            print(str(e))

    return render(request, 'login.html')

def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user_obj = User.objects.filter(username=username)

            if user_obj.exists():
                messages.error(request, 'Username already taken')
                return redirect('/register/')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request, "Account Created")
            return redirect('/login/')
        except Exception as e:
            print(str(e))


    return render(request, 'register.html')

@login_required(login_url='/login/')
def add_Cart(request, pizza_uid):
    user = request.user
    pizza_obj = Pizza.objects.get(uid=pizza_uid)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)
    cart_items = CartItems.objects.create(cart=cart, pizza=pizza_obj)
    return redirect('/')


@login_required(login_url='/login/')

def cart(request):
    cart = Cart.objects.get(is_paid=False, user=request.user)

    

    response = api.payment_request_create(
        amount=cart.get_cart_total(),
        purpose="Order",
        buyer_name=request.user.username,
        email="brajesh.bm92@gmail.com",
        redirect_url='http://127.0.0.1:8000/success/',
    )

    context = {'cart': cart,#cart, 'payment_url': response['payment_request']['longurl']
               }
    print(response)

    return render(request, 'cart.html', context)


@login_required(login_url='/login/')

def remove_cart_items(request, cart_item_uid):
    try:
        cart_item = CartItems.objects.get(uid=cart_item_uid)
        cart_item.delete()
        return redirect('/cart/')
    except CartItems.DoesNotExist:
        messages.error(request, 'Cart item not found.')
        return redirect('/cart/')
    except Exception as e:
        print(str(e))
        messages.error(request, 'An error occurred.')
        return redirect('/cart/')
    
@login_required(login_url='/login/')

def orders(request):
    orders = Cart.objects.filter(is_paid=True, user=request.user)
    context = {'orders': orders}
    return render(request, 'order.html', context)
