from django.contrib import admin
from .models import Message, Room
from django.contrib.admin import ModelAdmin


@admin.register(Room)
class RoomAdmin(ModelAdmin):
    list_display = ["name", "label"]
    search_fields = ["name"]
    sortable_by = ["created_at"]


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ["room", "user", "message", "timestamp"]
    search_fields = ["user"]
    sortable_by = ["timestamp"]
