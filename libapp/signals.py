from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from django.db.models.signals import post_save

@receiver(post_save,sender = User)
def create_profile(sender,instance,created,**kwargs):
    '''
    this function creates a profuile for the user on registration
    '''
    if created:
        Profile.objects.create(user = instance)
@receiver(post_save, sender = User)
def save_profile(sender, instance,**kwargs):
    '''
    this function saves a profile on creation of a new user
    '''
    instance.profile.save()
    