from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserLoginHistory

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'status', 'is_staff', 'is_active')
    list_filter = ('role', 'status', 'is_staff', 'is_active', 'date_inscription')
    search_fields = ('email', 'first_name', 'last_name', 'telephone')
    ordering = ('-date_inscription',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'telephone', 'adresse', 'ville', 'photo')}),
        ('Statut et rôles', {'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('date_inscription', 'last_login')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'status'),
        }),
    )

class UserLoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'login_time', 'ip_address', 'login_success')
    list_filter = ('action', 'login_success', 'login_time')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'ip_address')
    ordering = ('-login_time',)
    readonly_fields = ('login_time',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserLoginHistory, UserLoginHistoryAdmin)
