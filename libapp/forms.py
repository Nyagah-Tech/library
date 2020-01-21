from django.contrib.auth.models import User
from django import forms
from .models import *

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = [
            'name',
            'author',
            'category',
            'description',
            'published_date',
            'fee',
        ]

class borrowform(forms.ModelForm):
    class Meta:
        model = Borrowing
        exclude = {
            'book_id',
            'user_id',
            'borrowed_on',
            'penalty',
            'total_fee',
        }
            