from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'telephone', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Informations BEST AÉROS Gabon', {'fields': ('role', 'telephone', 'whatsapp', 'photo_profil')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations BEST AÉROS Gabon', {'fields': ('role', 'telephone', 'whatsapp', 'photo_profil')}),
    )
