from django.shortcuts import redirect, render, HttpResponse
from django.contrib import messages
from .models import *
import random

def index(request):
    if "user_id" in request.session:
        return redirect('/pizza')
    return render(request, "index.html")

def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request,"Invalid email/password")
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/pizza')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        user = User.objects.register(request.POST)
        request.session['user_id'] = user.id
        return redirect('/pizza')

def logout(request):
    request.session.flush()
    return redirect('/')


def pizza(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=request.session['user_id'])
    orders = Pizza.objects.all()
    all_orders = user.orders.all()
    context = {
        'user': user,
        'orders' : orders,
        'all_orders': all_orders,
    }
    return render(request, 'home.html', context)

def account(request, id):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=request.session['user_id'])
    all_orders = user.orders.all()
    orders = Order.objects.all().order_by("-created_at")
    context = {
        'user': user,
        'orders' : orders,
        'all_orders': all_orders,
    }

    return render(request, 'account.html', context)

def update(request, id):
    user = User.objects.get(id=request.session['user_id'])
    errors = User.objects.updateaccount_validator(request.POST)
    if len(errors) > 0:

        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account/'+ str(id))
    else:
        user.fname = request.POST['firstname']
        user.lname = request.POST['lastname']
        user.email = request.POST['updated_email']
        user.address = request.POST['updated_address']
        user.city = request.POST['updated_city']
        user.state = request.POST['updated_state']
        user.save()
        return redirect('/account/'+ str(id))


def create(request):
    user = User.objects.get(id=request.session['user_id'])
    context= {
        'user': user,
    }
    return render(request, 'craft.html', context)

def add(request):
    if 'user_id' not in request.session:
        return redirect('/login')

    costype = [{"name": "VEGETERIAN", "cost":5}, {"name": "PEPERONI", "cost":6}, {"name": "MARGHERITA", "cost":3},{"name": "HAWAII", "cost":8},{"name": "BUFFALO", "cost":9},{"name": "BARBEQUE", "cost":7},{"name": "SUPREME", "cost":10}]
    for key  in costype:
        if key["name"]==request.POST['types']:
            costs=0
            costs=int(key["cost"])
    costsize= [{"name": "LARGE", "cost":5}, {"name": "MEDIUM", "cost":4}, {"name": "SMALL", "cost":3}]
    for key  in costsize:
        if key["name"]==request.POST['size']:
            costssize=0
            costssize=int(key["cost"])
    if request.POST['method'] =='Delivery':
        delivery_price=2
    else:
        delivery_price=0

    quantity=int(request.POST['qty'])

    pizzacosts=(costs+costssize)*quantity
    user = User.objects.get(id=request.session['user_id'])
    order=Order.objects.create(user=user,method=request.POST['method'],qty=quantity, price= pizzacosts, delivery_price=int(delivery_price))
    pizza=Pizza.objects.create(types=request.POST['types'],order=order,size=request.POST['size'],crust=request.POST['crust'])

    return redirect('/pizza/order/'+str(pizza.id))

def order(request, id):
    user = User.objects.get(id=request.session['user_id'])
    order = Order.objects.get(id=id)
    tax_price= (int(order.price) + int(order.delivery_price))*0.2
    total= int(order.price)+int(order.delivery_price)+int(tax_price)
    context = {
        'user' : user,
        'order': order,
        'tax_price': tax_price,
        'total': total,
    }     
    return render(request, 'order.html', context)

def favorite(request, id):
    user = User.objects.get(id=request.session['user_id'])
    order = Order.objects.get(id=id)
    user.favorites.add(order)
    return redirect('/account/'+ str(user.id))

def remove(request, id):
    user = User.objects.get(id=request.session['user_id'])
    order = Order.objects.get(id=id)
    user.favorites.remove(order)
    return redirect('/account/'+ str(user.id))

def createFavorite(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=request.session['user_id'])
    favorite = user.favorites.all() 
    if len(favorite)>0:
        fav_pizza = random.choice(user.favorites.all())
        order = Order.objects.create(user=user,method=fav_pizza.method,qty=fav_pizza.quantity, price= fav_pizza.price, delivery_price=int(fav_pizza.delivery_price))
        pizza=Pizza.objects.create(types=fav_pizza.pizza.types,order=order,size=fav_pizza.pizza.size,crust=fav_pizza.pizza.crust)
        return redirect('/pizza/order/'+str(pizza.id))
    else:
        messages.error(request, 'You dont have a favorite!!!')
        return redirect('/pizza')

def random(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    user = User.objects.get(id=request.session['user_id'])
    orders = user.orders.all() 
    if orders.count() == 0:
        messages.error(request, 'You dont have an order')
        return redirect('/pizza')
    else:
        random_pizza = random.choice(user.orders.all())
        order = Order.objects.create(user=user,method=random_pizza.method, qty=random_pizza.quantity, price=random_pizza.price, delivery_price=int(random_pizza.delivery_price))
        pizza=Pizza.objects.create(types=random_pizza.pizza.types,order=order,size=random_pizza.pizza.size,crust=random_pizza.pizza.crust)
        return redirect('/pizza/order/'+str(pizza.id)) 