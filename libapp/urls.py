from django.conf import settings
from django.urls import path,include
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path('view/book/<int:book_id>',views.borrow_view,name="borrow"),
    path('books/category/<int:id>',views.category_view,name='category'),
    path('comment/book/<int:id>',views.comment_view,name="comment"),
    path('rate/book/<int:id>',views.rate_view,name='rate'),
    path('penalty/<int:id>',views.penalty,name="penalty"),
    path('profile/',views.profile_view,name='profile'),
    path('view/notify/',views.user_communicate,name="communicate"),
    path('pay/penalty/',views.pay_penalty,name="pay_penalty"),

    #dashboard
    path('dashboard/',views.dashboard,name="user_dashboard"),
    path('users/',views.registered_users,name="system_users"),
    path("user/activate/<int:id>",views.user_activate,name="activate_user"),
    path("user/deactivate/<int:id>",views.user_deactivate,name="deactivate_user"),
    path("add/book",views.add_book,name="add-book"),
    path("notification/",views.notification,name="notification"),
    path("user/notification/<int:id>",views.add_user_notify,name="add-notify"),
    path("all/notifications/",views.all_notes,name="all-notes"),
    path("all-books/",views.all_books,name = "all_books"),
    path("update-book/<int:id>",views.edit_book,name="update-book"),
    path("delete-book/<int:book_id>",views.delete_book,name="delete-book"),
    path("search-book/",views.search_book_by_name,name="search"),
    path("all-categories/",views.get_all_categories,name = "all-categories"),
    #paypal
    path("paypal/",include('paypal.standard.ipn.urls')),
    path("process-payment/",views.process_payment,name="process_payment"),
    path('payment-done/', views.payment_done, name='payment-done'),
    path('payment-cancelled/', views.payment_canceled, name='payment-cancelled'),
    path('q-forex-binary-f-k-defw-dshsgdtdhvdsss-scczzc-url/',include('paypal.standard.ipn.urls')),
    path("penalty-payment/",views.penalty_payment,name="penalty_payment")
    
    
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)