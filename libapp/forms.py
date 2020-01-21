from django.contrib.auth.models import User
from django import forms
from .models import *

class Books(forms.ModelForm):
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