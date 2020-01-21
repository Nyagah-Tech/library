from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Books(models.Model):
    '''
    this is a class that defines the structure in which a book will take to be saved in a db
    '''
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete= models.CASCADE)
    description = HTMLField()
    pic = models.ImageField(upload_to='books/',blank=True)
    published_date = models.DateField(auto_now_add=False)
    fee = models.IntegerField(default = 0)
    
    
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    '''
    this class defines the rating of the books
    '''
    content = models.IntegerField(default=1)
    theme = models.IntegerField(default = 1)
    physical_appearance = models.IntegerField(default  = 1)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    book_id = models.ForeignKey(Books,on_delete = models.CASCADE)
    
    
class Borrowing(models.Model):
    '''
    this is a class that defines the borrowing mechanism of a user
    '''
    book_id = models.ForeignKey(Books,on_delete= models.CASCADE)
    user_id = models.ForeignKey(User,on_delete = models.CASCADE)
    total_fee = models.IntegerField(default=0)
    borrowed_on = models.DateTimeField(auto_now_add=True)
    due_on = models.DateTimeField(auto_now_add=False)
    penalty = models.IntegerField(default=0)
    
    def __str__(self):
        return self.book_id
    
class Profile(models.Model):
    '''
    this class gives a blueprint on how a profile is made
    '''
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile_pic = models.ImageField(upload_to= 'images/', default= 'default.jpg')
    bio = HTMLField()
    update_on = models.DateTimeField(auto_now_add=True)
    delete_on = models.DateTimeField(blank = True,null = True)
    
    def __str__(self):
        return self.user.username
    