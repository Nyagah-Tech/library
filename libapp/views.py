from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import *

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
    return render(request,'all/home.html')

@login_required()
def borrow_view(request,book_id):
    if request.method == 'POST':
        book = get_object_or_404(Books,id = book_id)
        form = borrowform(request.POST)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.book_id = id
            item.user_id = request.user
            item.total_fee = book.fee
            item.penalty = 0
            item.save()
            return redirect('home')
        else :
            messages.info(request,'all fields are required')
            return redirect('borrow',id = book.id)
    else:
        form = borrowform()
        book = get_object_or_404(Books,id = book_id)
        context = {
            'book':book,
            'form':form,
        }
        return render(request,'all/single_book.html',context)