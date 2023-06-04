from django.contrib import admin
from .models import User
from django.contrib.admin import ModelAdmin


@admin.register(User)
class AuthUserAdmin(ModelAdmin):
    list_display = ["email", "username", "created_at", "is_active"]
    search_fields = ["email"]
    sortable_by = ["created_at"]
