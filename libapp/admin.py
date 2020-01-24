from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Borrowing)
admin.site.register(Rating)
admin.site.register(Books)
admin.site.register(Category)
admin.site.register(Notification)