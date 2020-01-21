from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name="home"),
    path('view/book/<int:id>',views.borrow_view,name="borrow"),
    
]