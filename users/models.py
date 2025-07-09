from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    farmer = models.BooleanField(default=False)
    agronomist = models.BooleanField(default=False)
    extension_worker = models.BooleanField(default=False)
    
    def get_user_role(self):
        """Returns the user's role as a string"""
        if self.farmer:
            return 'farmer'
        elif self.agronomist:
            return 'agronomist'
        elif self.extension_worker:
            return 'extension_worker'
        return None
    
    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Check if profile exists before trying to save it
    if hasattr(instance, 'profile'):
        instance.profile.save()
    else:
        # Create profile if it doesn't exist
        Profile.objects.create(user=instance)
