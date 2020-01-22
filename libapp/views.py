from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib.auth.decorators import permission_required
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import random
from django.views.decorators.csrf import csrf_exempt
from django.http.response import json,JsonResponse


# Create your views here.

def registration(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']

        if password1 == password:
            if User.objects.filter(username=username):
                messages.info(request, 'This Username is taken!')
                return redirect('registration')
            elif User.objects.filter(email=email):
                messages.info(request, 'This Email is taken!')
                return redirect('registration')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)   
                user.save()           
                
                return redirect('home')
        else:
            messages.info(request,'Passwords should match!')
            return redirect('registration')
    else:
        return render(request,'auth/registration.html')
@login_required()
def home(request):
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }
    
    return render(request,'all/home.html',context)

@login_required()
def borrow_view(request,book_id):
    if request.method == 'POST':
        book = get_object_or_404(Books,id = book_id)
        form = borrowform(request.POST)
       
        
        
        if form.is_valid():
            number = request.POST.get('number')
            email = request.POST.get('email')
            if User.objects.filter(email = email).first() is None:
                messages.info(request,'Invalid email')
                return redirect('borrow', book_id = book.id)
            else:
                item={
                    'bookId':book_id,
                    'user_id':request.user.id,
                    'total_fee':book.fee * int(number),
                } 
                
                request.session['order']=item
                return redirect('process_payment')
        else :
            messages.info(request,'all fields are required')
            return redirect('borrow',book_id = book.id)
    else:
        form = borrowform()
        book = get_object_or_404(Books,id = book_id)
        context = {
            'book':book,
            'form':form,
        }
        return render(request,'all/single_book.html',context)
    
@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required()
def category_view(request,id):
    books = Books.objects.filter(category = id)
    
    context = {
        'books':books,
    }
    return render(request,'all/category.html',context)

#paypal
#---------------------------------------------------------------
@login_required()
def process_payment(request):
    item = request.session.get('order')
    
    book = Books.objects.get(id = item["bookId"])
    
    if item["total_fee"] != 0:
        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':item["total_fee"],
            'item_name':'{}'.format(book.name),
            'invoice':str(random.randint(0000,9999)),
            'currency_code':'USD',
            'notify_url': "https://library.herokuapp.com/",
            'return_url':"https://library.herokuapp.com/",
            'cancel_return': 'https://forex254.herokuapp.com/payment-cancelled/',
        }
        
        
    
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request,'paypal/process_payment.html',{"item":item,"form":form})
    else:
        messages.info(request,'you should input the number of books you need!')
        return redirect('borrow',book_id = book.id)
#ADMIN DASHBOARD
#--------------------------------------------------------------
@login_required()
@permission_required("True", "home")
def registered_users(request):
    users = User.objects.all()
    context = {
        'users':users,
    }
    return render(request,'admin_site/users.html',context)

@login_required()
@permission_required("True", "home")
def user_deactivate(request,user_id):
    user = User.objects.get(pk = user_id)
    user.is_active = False
    user.save()
    messages.success(request,f"{user.username}'s account has been deactivated")
    return redirect("system_users")

@login_required()
@permission_required("True","home")
def user_activate(request,user_id):
    user = User.objects.get(pk = user_id)
    user.is_active = True
    user.save()
    messages.success(request,f"{user.username}'s account has been activated ")
    return redirect("system_users")

@login_required()
@permission_required("True","home")
def  dashboard(request):
    return render(request,'admin_site/dashboard.html')

@login_required()
@permission_required("True","home")
def add_book(request):
    if request.method == 'POST':
        form = BooksForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("system_users")
        else:
            messages.info(request,['All fields are required'])
            return redirect('add-book')
    else:
        form = BooksForm()
        context = {
            "form":form,
        }
        return render(request,'admin_site/add_book.html',context)
        
        
        
        
        
#END ADMIN
#-----------------------------------------------------

    
