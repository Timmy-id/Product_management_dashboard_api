from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'avatar_preview')

    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:contain;" />',
                obj.avatar.url
            )
        return "No Image"

    avatar_preview.short_description = 'Avatar Preview'

admin.site.register(CustomUser, CustomUserAdmin)