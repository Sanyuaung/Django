from django.contrib.auth.models import Group
from accounts.decorators import admin_only, authenticated_user,allowed_roles
from django.forms.models import inlineformset_factory
from django.shortcuts import render,redirect
from django.http import HttpResponse, request
from accounts.models import *
from accounts.forms import *
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required



@login_required(login_url='/login')
@allowed_roles(roles=['Admin'])
def customers(request,id):
    customer=Customer.objects.get(id=id)
    orders=customer.order_set.all()
    order_count=orders.count()
    filterObj=OrderFilter(request.GET,queryset=orders)
    orders=filterObj.qs
    return render(request,'accounts/customers.html',{
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'filterObj':filterObj
    })


@login_required(login_url='/login')
@allowed_roles(roles=['Customer'])
def customers_profile(request):
    orders=request.user.customer.order_set.all()
    total=orders.count()
    delivered=orders.filter(status="delivered").count()
    pending=orders.filter(status="pending").count()
    return render(request,'accounts/customers_profile.html',{
        'orders':orders,
        'total':total,
        'delivered':delivered,
        'pending':pending
    })


def customers_profile_setting(request):
    form=CustomerProfile(instance=request.user.customer)
    if request.method=="POST":
        form=CustomerProfile(request.POST,request.FILES,instance=request.user.customer)
        form.save()
        return redirect('/customers_profile')
    return render(request,'accounts/profile_setting.html',{
        'form':form
    })

@login_required(login_url='/login')
@allowed_roles(roles=['Admin'])
def products(request):
    products=Product.objects.all()
    return render(request,'accounts/products.html',{
        'products':products
    })


@login_required(login_url='/login')
@admin_only
def dashboard(request):
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total=orders.count()
    delivered=Order.objects.filter(status="delivered").count()
    pending=Order.objects.filter(status="pending").count()
    return render(request,'accounts/dashboard.html',{
        'customers':customers,
        'orders':orders,
        'total':total,
        'delivered':delivered,
        'pending':pending
    })


@login_required(login_url='/login')
@allowed_roles(roles=['Admin'])
def orderCreate(request,customerId):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=customerId);
    formset=OrderFormSet(instance=customer,queryset=Order.objects.none())
    if request.method=="POST":
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save();
            return redirect('/');            

    return render(request,'accounts/order_form.html',{
        'formset':formset
    })


@login_required(login_url='/login')
@allowed_roles(roles=['Admin'])
def orderUpdate(request,orderId):
    order=Order.objects.get(id=orderId);
    form=OrderForm(instance=order)
    if request.method=="POST":
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save();
            return redirect('/');            

    return render(request,'accounts/order_form.html',{
        'form':form
    })
    

@login_required(login_url='/login')
@allowed_roles(roles=['Admin'])
def orderDelete(request,orderId):
    order=Order.objects.get(id=orderId);
    if request.method=="POST":
        order.delete();
        return redirect('/');
                
    return render(request,'accounts/order_delete.html',{
        'order':order
    })


@authenticated_user
def register(request):
    form=RegisterForm()
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save();
            
            login(request,user)
            return redirect('/')
    return render(request,'accounts/register.html',{
        'form':form
    })

@authenticated_user
def userlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else :
            messages.error(request,'username and password is incorrect')
            return redirect('/login')
    return render(request,'accounts/login.html')


@login_required(login_url='/login')
def userlogout(request):
    logout(request)
    return redirect('/login')




# Create your views here.
