from django.contrib import admin
from .models import CustomUser, Chat, Message

admin.site.register(CustomUser)
admin.site.register(Message)
admin.site.register(Chat)

