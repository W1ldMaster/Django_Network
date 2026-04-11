from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile


class CustomUserAdmin(UserAdmin):
    # Проверьте, нет ли здесь 'image'
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные поля', {'fields': ('avatar',)}),  # ← avatar, не image
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные поля', {'fields': ('avatar',)}),  # ← avatar, не image
    )


# Register your models here.

admin.site.register(UserProfile, CustomUserAdmin)