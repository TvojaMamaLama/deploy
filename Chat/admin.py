from django.contrib import admin

from .models import Chat, Room, User


admin.site.register(Chat)
admin.site.register(Room)
admin.site.register(User)
