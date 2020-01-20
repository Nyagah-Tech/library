from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class Books(models.Model):
    '''
    this is a class that defines the structure in which a book will take to be saved in a db
    '''
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = HTMLField()
    published_date = models.DateField

class Rating(models.Model):
    '''
    this class defines the rating of the books
    '''
    content = models.IntegerField(default=1)
    theme = models.IntegerField(default = 1)
    physical_appearance = models.IntegerField(default  = 1)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    book_id = models.ForeignKey(Books,on_delete = models.CASCADE)
    

# Create your models here.
