from django.contrib import admin
from .models import User, UserGroup

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "user_group", "created_at")
    search_fields = ("username", "email")

@admin.register(UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ("id", "group_name")