from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from . models import *
from . forms import *
import stripe
from django.http import HttpResponse

stripe.api_key = 'sk_test_z65UX1GwYTZJrCR58iZcQfQJ00jiPLf5zG' #stripe api key


# Create your views here.
def index(request):
    plans = Plan.objects.all()
    context = {'plans':plans}
    return render(request,'base/index.html',context)




#login function
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated: #if user authenticate then automatically go to index page 
        return redirect('index')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request,'User doest not exist.')
        
        user = authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Login Successfully.')
            return redirect('index')
        else:
            messages.error(request,'email OR password doest not exist.')
    context={'page':page}
    return render(request,'base/login_register.html',context)




#Register function
def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'An error occured during registration.')

    context = {'form':form}
    return render(request,'base/login_register.html',context)




#logout function
def Userlogout(request):
    logout(request)
    return redirect('index')




#Check out function
@login_required(login_url='login')
def checkout(request):
    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    coupons = {'mehedi':31, 'welcome':10} 

    if request.method == 'POST':
        stripe_customer = stripe.Customer.create(email=request.user.email, source=request.POST['stripeToken'])
        plan = 'price_1JiGJgEcjDyQJdh0J2Hgi3k1' #bronze plan stripe key
        if request.POST['plan'] == 'silver':
            plan = 'price_1JiGJgEcjDyQJdh0pLWYKrJC'  #silver plan stripe key
        if request.POST['plan'] == 'gold':
            plan = 'price_1JiGJgEcjDyQJdh05C5J1u8M'   #gold plan stripe key
        if request.POST['coupon'] in coupons:
            percentage = coupons[request.POST['coupon'].lower()]
            try:
                coupon = stripe.Coupon.create(duration='once', id=request.POST['coupon'].lower(),
                percent_off=percentage)
            except:
                pass
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'plan':plan}], coupon=request.POST['coupon'].lower())
        else:
            subscription = stripe.Subscription.create(customer=stripe_customer.id,
            items=[{'plan':plan}])

        customer = Customer()          #Customer model
        customer.user = request.user
        customer.stripeid = stripe_customer.id
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = subscription.id
        customer.save()

        return redirect('settings')
    else:
        coupon = 'none'
        plan = 'bronze'
        price = 50000
        og_dollar = 500
        coupon_dollar = 0
        final_dollar = 500
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'silver':
                plan = 'silver'
                price = 75000
                og_dollar = 750
                final_dollar = 750
        if request.method == 'GET' and 'plan' in request.GET:
            if request.GET['plan'] == 'gold':
                plan = 'gold'
                price = 150000
                og_dollar = 1500
                final_dollar = 1500
        if request.method == 'GET' and 'coupon' in request.GET:
            print(coupons)
            if request.GET['coupon'].lower() in coupons:
                print('fam')
                coupon = request.GET['coupon'].lower()
                percentage = coupons[request.GET['coupon'].lower()]


                coupon_price = int((percentage / 100) * price)
                price = price - coupon_price
                coupon_dollar = str(coupon_price)[:-2] + '.' + str(coupon_price)[-2:]
                final_dollar = str(price)[:-2] + '.' + str(price)[-2:]
        
        context = {'plan':plan,'coupon':coupon,'price':price,'og_dollar':og_dollar,
        'coupon_dollar':coupon_dollar,'final_dollar':final_dollar}

        return render(request, 'base/checkout.html',context)



#setting function
def settings(request):
    customer = Customer.objects.filter(user_id=request.user.id)
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    
    context = {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end,'customer':customer}
    return render(request, 'base/settings.html', context)



#update account function
@user_passes_test(lambda u: u.is_superuser)
def updateaccounts(request):
    customers = Customer.objects.all()
    for customer in customers:
        subscription = stripe.Subscription.retrieve(customer.stripe_subscription_id)
        if subscription.status != 'active':
            customer.membership = False
        else:
            customer.membership = True
        customer.cancel_at_period_end = subscription.cancel_at_period_end
        customer.save()
    return HttpResponse('completed')





