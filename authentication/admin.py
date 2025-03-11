from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, RegistrationOTP

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'phone_number', 'user_type', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('email', 'name', 'phone_number')
    readonly_fields = ('date_joined',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('name', 'phone_number')}),
        ('Permissions', {'fields': ('user_type', 'is_active', 'is_staff', 'is_superuser', 'is_verified')}),
        ('Important Dates', {'fields': ('date_joined', 'last_login')}),
        ('Groups', {'fields': ('groups',)}),
        ('User Permissions', {'fields': ('user_permissions',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_number', 'user_type', 'password1', 'password2'),
        }),
    )

class RegistrationOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'user_type', 'code', 'created_at', 'expires_at', 'is_valid_display')
    list_filter = ('user_type', 'created_at')
    search_fields = ('email', 'name', 'code')
    readonly_fields = ('code', 'created_at', 'expires_at')
    
    def is_valid_display(self, obj):
        is_valid = obj.is_valid()
        if is_valid:
            return format_html('<span style="color: green;">Valid</span>')
        return format_html('<span style="color: red;">Expired</span>')
    
    is_valid_display.short_description = 'Valid'

# Register models with custom admin classes
admin.site.register(User, UserAdmin)
admin.site.register(RegistrationOTP, RegistrationOTPAdmin)