from django.shortcuts import render , get_object_or_404
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib import messages
import razorpay
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
import re
from .utils import *
from django.contrib.auth.models import User
from cart.cart import Cart


# Create your views here.
def base(request):
    return render(request, 'base.html')

def home(request, category_id=None):
    sliders=slider.objects.all()
    cat=category.objects.all()
    pro=Product.objects.all()

    cat_id = request.GET.get('category')
    if cat_id:
        pro = Product.objects.filter(category_id =cat_id)
    else:
        pro = Product.objects.all()


    context={
        'sliders' : sliders,
        'cat':cat,
        'pro':pro,
    }
    return render(request, 'home.html', context)

def product_detail(request, slug):
    pro=Product.objects.filter(slug=slug)

    if pro.exists():
        pro=Product.objects.get(slug=slug)
    else:
        return redirect('error')
        
    cat=category.objects.all()
    context={
        'cat':cat,
        'pro':pro,
    }
    return render(request, 'product_detail.html' , context)

def error(request):
    return render(request,'error.html')




#==================ACCOUT VIEWS FUN()===================#

def account(request):
    return render(request,'login.html')

def rigester(request):
    if request.method == "POST":
        data=request.POST

        username=data.get('username')
        email=data.get('email')
        name=data.get('first_name')
        password=data.get('password')

        person=User.objects.filter(username=username)
        if person.exists():
            messages.info(request,'USERNAME OR EMAIL HAS BEEN USED BEFORE !')
            return redirect('login/')
        
        person=User.objects.filter(email=email)
        if person.exists():
            messages.info(request,'USERNAME OR EMAIL HAS BEEN USED BEFORE !')
            return redirect('login/')
        else:
            person=User(
                username=username,
                email=email,
                first_name=name,
            )

            person.set_password(password)
            person.save()
            messages.info(request,'Account has been created succesfully')   
            return redirect('login/')




def login_user(request):
    if request.method=="POST":
        data=request.POST

        username=data.get('username')
        password=data.get('password')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Please make an amount first')   
            return redirect('login/')
        
@login_required
def profile(request):
    return render(request,'profile.html')


def profile_update(request):
    if request.method=="POST":
        data=request.POST

        first_name=data.get('first_name')
        username=data.get('username')
        email=data.get('email')
        password=data.get('password')
        user_id=request.user.id

        user=User.objects.get(id=user_id)
        user.first_name=first_name
        user.username=username
        user.email=email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'updated Successfully')   
        return redirect('profile')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


# def shop(request):
#     pros = Product.objects.all()  # Get all products
   
#     # Retrieve categories for filtering
#     cat = category.objects.all()

#     context = {
#         'pro': pros,
#         'cat': cat,
#     }

#     return render(request, 'shop.html', context)


def shop(request):
    cat = category.objects.all()
    cat_id = request.GET.get('category')
    pro = Product.objects.all()

    if cat_id:
        pro = Product.objects.filter(category_id =cat_id)
    else:
        pro = Product.objects.all()


    context = {'cat': cat, 'pro': pro}
    return render(request, 'shop.html', context)


#===================CART VIEWS===================#

@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    messages.info(request,'your quantity of ')   
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    messages.info(request,'your quantity of ')   
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    cart=request.session.get('cart')
    packing_cost=sum(i['packing_cost'] for i in cart.values() if i)
    tax=sum(i['tax'] for i in cart.values() if i )
    delivery_charge = sum(i.get('delivery_charge', 200) for i in cart.values() if i)
    context={
        'cp':packing_cost,
        't':tax,
        'dc':delivery_charge,
    }
    return render(request, 'cart.html' , context)


@csrf_exempt
def placeorder(request):
    context = {}

    cart = request.session.get('cart')
    packing_cost = sum(i['packing_cost'] for i in cart.values() if i)
    tax = sum(i['tax'] for i in cart.values() if i)
    delivery_charge = sum(i.get('delivery_charge', 200) for i in cart.values() if i)

    mj = {
        'cp': packing_cost,
        't': tax,
        'dc': delivery_charge,
    }

    if request.method == "POST":
        data = request.POST
        cart = request.session.get('cart')

        user = request.user
        user_id = request.session.get('_auth_user_id')
        user = User.objects.get(id=user_id)
        first_name = data.get('first_name')
        email = data.get('email')
        country = data.get('country')
        address = data.get('address')
        city_town = data.get('city_town')
        state = data.get('state')
        pincode = data.get('pincode')
        phone = data.get('phone')
        amount = data.get('amount')
        order_id = data.get('order_id')

        order = Order.objects.create(
            user=user,
            first_name=first_name,
            email=email,
            country=country,
            address=address,
            city_town=city_town,
            state=state,
            pincode=pincode,
            phone=phone,
            amount=amount,
        )

        for i in cart:
            a = cart[i]['price']
            b = cart[i]['quantity']
            total = a * b

            item = OrderItem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total,
            )
            item.save()

        amount_value = re.findall(r'\d+', amount)
        amount_in_rupees = int(amount_value[0])

        client = razorpay.Client(auth=(settings.KEY, settings.SECRET_KEY))
        data = {"amount": amount_in_rupees * 100, "currency": "INR", "receipt": "1"}
        payment = client.order.create(data=data) # type: ignore
        order.razorpay_order_id = payment['id']  # Assign 'razorpay_order_id' to the order object
        order.save()

        context = {
            'order_id': order_id,
            'payment': payment,
        }

        return render(request, "placeorder.html", {**context, **mj})


@login_required(login_url="/accounts/login/")
def checkout(request):
    cart=request.session.get('cart')
    packing_cost=sum(i['packing_cost'] for i in cart.values() if i)
    tax=sum(i['tax'] for i in cart.values() if i )
    delivery_charge = sum(i.get('delivery_charge', 200) for i in cart.values() if i)

    # orders = Order.objects.values('amount')

    # for order in orders:
    #     amount = order['amount']


    # client = razorpay.Client(auth=("rzp_test_OtnyCkMugM2rxH", "qKEILi75jXLtrtYlZ3jfpJCI"))
    # data = {"amount": 100 * 100, "currency": "INR", "receipt": "order_rcptid_11"}
    # payment = client.order.create(data=data)

    context={
            'cp':packing_cost,
            't':tax,
            'dc':delivery_charge,
           
        }
    
    return render(request,'checkout.html',context)

@csrf_exempt
def thankyoupage(request):
    return render(request,'thankyou.html')

from django.core.exceptions import MultipleObjectsReturned


@csrf_exempt
def success(request):
    order_id = request.GET.get('razorpay_order_id')
    try:
        order = Order.objects.get(razorpay_order_id=order_id)
        order.paid = True
        order.save()
        send_email_to_client(order)
        return render(request, 'thankyou.html')
    except Order.DoesNotExist:
        return HttpResponse("Order matching query does not exist.")
    except MultipleObjectsReturned:
        orders = Order.objects.filter(razorpay_order_id=order_id)
        # Decide how to handle multiple orders with the same razorpay_order_id
        # For example, you can mark all the orders as paid or choose a specific order
        # Here, we are marking the first order as paid and the rest as unpaid
        for i, order in enumerate(orders):
            if i == 0:
                order.paid = True
            else:
                order.paid = False
            order.save()
        return render(request, 'thankyou.html')
    


def myorder(request):
    user = request.user
    orders = OrderItem.objects.filter(user_id=user)
    context={
        'orders':orders
    }
    return render(request, 'myorder.html',context)



def cancel_order(request, id):
    if request.method == 'POST':
        order = OrderItem.objects.filter(id=id)
        order.delete()
        send_user(order)
        messages.success(request, 'Order successfully cancelled.')
        return redirect('myorder')
    else:
        return render(request, 'confirmation.html', {'order_id': id})
    

def myorderji(request):
    return render(request,'orderji.html')