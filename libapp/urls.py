from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path('view/book/<int:book_id>',views.borrow_view,name="borrow"),
    path('books/category/<int:id>',views.category_view,name='category'),
    #dashboard
    path('dashboard/',views.dashboard,name="user_dashboard"),
    path('users/',views.registered_users,name="system_users"),
    path("user/activate/<int:id>",views.user_activate,name="activate_user"),
    path("user/deactivate/<int:id>",views.user_deactivate,name="deactivate_user"),
    path("add/book",views.add_book,name="add-book"),
    #paypal
    path("paypal/",include('paypal.standard.ipn.urls')),
    path("process-payment/",views.process_payment,name="process_payment"),
    
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)