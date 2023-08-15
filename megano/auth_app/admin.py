from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Регистрация модели Профиль в админке"""

    list_display = ["pk", "fullName", "user", "avatar"]
    list_display_links = ["pk", "fullName"]
    ordering = ["pk"]
