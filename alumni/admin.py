from django.contrib import admin
from .models import college, chat_room_messages
# Register your models here.

admin.site.register(college)
admin.site.register(chat_room_messages)