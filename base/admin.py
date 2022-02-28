from django.contrib import admin

# Register your models here.

#buradaki Room models'ten geliyor..
from .models import Room, Topic, Message
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)