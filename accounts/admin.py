from django.contrib import admin
from .models import User, Profile




@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'created_at')
    search_fields = ('user__email',)
    ordering = ('user',)