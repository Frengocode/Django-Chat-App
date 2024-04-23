from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField


class CustomUser(AbstractUser):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', )
    birthday_date = models.DateField(null=True)
    profile_info = models.CharField(max_length=50, blank=True)
    country = CountryField()
    created_in = models.DateTimeField(auto_now_add=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscribe_field')


    class Meta:
        ordering = ['-created_in']

class Chat(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    img_file = models.ImageField(upload_to='image_message/', blank=True, null=True)
    

    class Meta:
        ordering = ['-timestamp']



class UserToDo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    to_do = models.CharField(max_length=1000)
    img = models.ImageField(upload_to='to_do_img/', blank=True)


    def __str__(self):
        return self.to_do
    
    class Meta:
        ordering = ['-created_at']
