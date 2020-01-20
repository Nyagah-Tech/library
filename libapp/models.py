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



# Create your models here.
