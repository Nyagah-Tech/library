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
            'pic',
        ]

class borrowform(forms.ModelForm):
    class Meta:
        model = Borrowing
        exclude = [
            'book_id',
            'user_id',
            'borrowed_on',
            'penalty',
            'total_fee',
            'no_of_books',
        ]
            
class commentform(forms.ModelForm):
    class Meta:
        model = Comment
        exclude =[
            'posted_by',
            'posted_on',
            'book_id',
        ]

            
class UserUpdateform(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]

class UpdateProfileForm(forms.ModelForm):
    bio = forms.Textarea()
    class Meta:
        model = Profile
        exclude =[
            'updated_on',
            'user',
            'delete_on',
        ]

class User_note_form(forms.ModelForm):
    class Meta:
        model = User_notification
        exclude = [
            'posted_by',
            'posted_on'
        ]