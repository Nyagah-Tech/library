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
    users = Borrowing.objects.filter(user_id_id = request.user.id)
    for user in users :
        if user.notification :
            return redirect('penalty',id=user.book_id_id)
    categories = Category.objects.all()
    context = {
        'categories':categories,
    }  
    return render(request,'all/home.html',context)
@login_required()
def penalty(request,id):
    users = Borrowing.objects.filter(user_id_id = request.user.id)
    for user in users :
        if user.notification :
            form = User_note_form()
          
            return render(request,'all/penalty.html',{"user":user,"form":form})
   
    


@login_required()
def borrow_view(request,book_id):
    if request.method == 'POST':
        book = get_object_or_404(Books,id = book_id)
        form = borrowform(request.POST)
       
        
        
        if form.is_valid():
            number = request.POST.get('number')
            total_fee = book.fee*int(number)
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
                borrow = Borrowing(book_id = book,
                                   user_id = request.user,
                                   total_fee = total_fee,
                                   no_of_days = number,
                                   no_of_books = number,
                                    )
                borrow.save()
                
                request.session['order']=item
                return redirect('process_payment')
            
        else :
            messages.info(request,'all fields are required')
            return redirect('borrow',book_id = book.id)
    else:
        form = borrowform()
        book = get_object_or_404(Books,id = book_id)
        comment_form= commentform()
        comments = Comment.objects.filter(book_id = book_id)
        rates = Rating.objects.filter(book_id = book_id)
        content=[]
        theme=[]
        physical=[]
        if rates:
            for rate in rates:
                content.append(rate.content)
                theme.append(rate.theme)
                physical.append(rate.physical_appearance)
            total = len(content) * 9
            content_rate = round(sum(content)/total * 100,2)
            theme_rate = round(sum(theme)/total * 100,2)
            physical_rate = round(sum(physical)/total *100)
            context = {
                'book':book,
                'form':form,
                'comment_form':comment_form,
                'comments':comments,
                'content_rate':content_rate,
                'theme_rate':theme_rate,
                'physical_rate':physical_rate,
            }
            return render(request,'all/single_book.html',context)
        else:
            theme_rate = 0
            physical_rate = 0
            content_rate = 0 
            context = {
                'book':book,
                'form':form,
                'comment_form':comment_form,
                'comments':comments,
                'content_rate':content_rate,
                'theme_rate':theme_rate,
                'physical_rate':physical_rate,
            }
            return render(request,'all/single_book.html',context)
    
@login_required()
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required()
def category_view(request,id):
    books = Books.objects.filter(category = id)
    category = Category.objects.get(id = id)
    
    context = {
        'books':books,
        'category':category,
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
            'notify_url': 'https://librarydan.herokuapp.com/q-forex-binary-f-k-defw-dshsgdtdhvdsss-scczzc-url/',
            'return_url':"https://librarydan.herokuapp.com/payment-done/",
            'cancel_return': "https://librarydan.herokuapp.com/payment-cancelled/",
        }
        
        
    
    
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request,'paypal/process_payment.html',{"item":item,"form":form})
    else:
        messages.info(request,'you should input the number of books you need!')
        return redirect('borrow',book_id = book.id)
    
@csrf_exempt
def payment_done(request):
    
    args={'post':request.POST,'get':request.GET}
        
    return render(request, 'paypal/payment_done.html',args)
 
 
@csrf_exempt
def payment_canceled(request):
    args={'post':request.POST,'get':request.GET}
    return render(request, 'paypal/payment_cancelled.html',args)

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
        
@login_required()
@permission_required("True","home")
def notification(request):
    user_borrow = Borrowing.objects.all()
    notification = Notification.objects.all()
    context = {
        "user_borrow":user_borrow,
        "notification":notification,
    }
    return render(request,'admin_site/notification.html',context)

@login_required()
@permission_required("True","home")
def add_user_notify(request,id):
    notification = get_object_or_404(Notification,id = id)
    if request.method =='POST':
        user_id = request.POST['note']
        book_id = request.POST['book']
        book = Books.objects.get(id=book_id)
        user = User.objects.get(id = user_id)
        borrower = Borrowing.objects.filter(user_id_id =user.id) 
        for borro in borrower:
            if borro.notification :
                notification.user.remove(user)
                notification.save()
                borro.notification = False
                borro.save()
                return redirect('add-notify',id=id)
            else: 
                notification.user.add(user)
                notification.save()
                borro.notification = True
                borro.save()
                return redirect('notification')
    else:
        messages.info(request,'process succesful')
        return redirect('notification')
        
@login_required()        
@permission_required("True","home")
def all_notes(request):
    notes = User_notification.objects.all()
    return render(request,'admin_site/all_note.html',{"notes":notes})

@login_required()
@permission_required("True","home")
def all_books(request):
    allBooks = Books.objects.all()
    context ={
        "allBooks":allBooks,
    }
    return render(request,"admin_site/allbooks.html",context)

@login_required()
@permission_required("True","home")
def edit_book(request,id):
    if request.method == 'POST':
        book = get_object_or_404(Books,id = id)
        book_form = BooksForm(request.POST,instance=book)
        if book_form.is_valid():
            updated_book = book_form.save()
            return redirect('all_books')
        else:
            messages.info(request,"please edit the book information")
            return redirect("update-book",id = book.id)
    else:
        book = get_object_or_404(Books,id = id)
        editBookForm  = BooksForm(instance=book)
        context ={
            "book":book,
            "editBookForm":editBookForm,
        }
        return render(request,"admin_site/Edit_book.html",context)
        
@login_required()           
@permission_required("True","home")
def delete_book(request,book_id):
    book = Books.objects.get(id = book_id)
    book.delete()
    return redirect("all_books")

@login_required()
@permission_required("True","home")
def search_book_by_name(request):
    if request.method == 'POST':
        search_term = request.POsT['searchterm']
        if search_term is None:
            messages.info(request,"please fill in the search input field")
            return redirect('all_books')
        else:
            books = Books.objects.filter(name = name)
            context={
                "books":books,
            }
            return render(request, "admin_site/search.html",context)
    else:
        return redirect('all_books')
@login_required()      
@permission_required("True","home")
def get_all_categories(request):
    categories = Category.objects.all()
    context={
        "categories":categories,
    }
    return render(request,"admin_site/all_categories.html",context)
          
#END ADMIN
#-----------------------------------------------------

@login_required()
def comment_view(request,id):
    book = Books.objects.get(id = id)
    if request.method =='POST':
        form = commentform(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.posted_by = request.user
            comment.book_id = book
            comment.save()
            return redirect('borrow',book_id = id)
        else:
            messages.info(request,'All fields are required')
            return redirect('borrow',book_id = id)
    else:
        messages.info(request,'Invalid operation')
        return redirect('borrow',book_id = id)
    
@login_required()
def rate_view(request,id):
    if request.method == 'POST':
        book = Books.objects.get(id=id)
        rates = Rating.objects.filter(book_id = id)
        for rate in rates:
            if rate.user== request.user:
                messages.info(request,'You have already rated the book')
                return redirect('category',id = book.category.id )
            
        book = Books.objects.get(id = id)
        content = request.POST.get('content')
        physical = request.POST.get('physical_appearance')
        theme = request.POST.get('theme')
        
        if book and content and physical and theme:
            rate = Rating(content = content,theme = theme,physical_appearance = physical,user = request.user,book_id = book)
            rate.save()
            return redirect('category',id = book.category.id)
        else:
            messages.info(request,'All fields are required')
            return redirect('category',id = book.category.id)

@login_required()
def profile_view(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST,request.FILES,instance=request.user.profile)
        form1 = UserUpdateform(request.POST,instance=request.user)
        if form.is_valid() and form1.is_valid():
            form1.save() 
            form.save()
            return redirect('profile')
    else:
        profile = Profile.objects.get(user = request.user)
        borrowed_books = Borrowing.objects.filter(user_id_id = request.user.id)
        form = UpdateProfileForm(instance=request.user.profile)
        form1 = UserUpdateform(instance=request.user)
        context ={
            'profile':profile,
            'borrowed_books':borrowed_books,
            'profile_form':form,
            'user_form':form1,
        }
        return render(request,'all/profile.html',context)

@login_required()
def user_communicate(request):
    if request.method == "POST":
        form = User_note_form(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.posted_by = request.user
            note.save()
            messages.info(request,'Your response has been recieved')
            return redirect('penalty',id = request.user.id)
        else:
            messages.info(request,'all fields are required')
            return redirect('penalty',id = request.user.id)
    else:
        return redirect('penalty', id= request.user.id)
    
@login_required()
def pay_penalty(request):
    if request.method == 'POST':
        total = request.POST['penalty']
        item ={
            "total_fee":total,
        }
           
        request.session['order']=item
        return redirect('penalty_payment')
    
@login_required()
def penalty_payment(request):
    item = request.session.get('order')
    
    if item["total_fee"] != 0:
        paypal_dict = {
            'business':settings.PAYPAL_RECEIVER_EMAIL,
            'amount':item["total_fee"],
            'item_name':'Product',
            'invoice':str(random.randint(0000,9999)),
            'currency_code':'USD',
            'notify_url': 'https://librarydan.herokuapp.com/q-forex-binary-f-k-defw-dshsgdtdhvdsss-scczzc-url/',
            'return_url':"https://librarydan.herokuapp.com/penalty-done/",
            'cancel_return': "https://librarydan.herokuapp.com/payment-cancelled/",
        }
        
        
    
        form = PayPalPaymentsForm(initial=paypal_dict)
        return render(request,'paypal/process_payment.html',{"item":item,"form":form})
    else:
        messages.info(request,'you should input the number of books you need!')
        return redirect('home')

@login_required()
def penalty_done(request):
    users = Borrowing.objects.filter(user_id_id = request.user.id)
    for user in users :
        if user.notification:
            user.notification = False
            user.save()
            return redirect('home')