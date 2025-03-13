from django.contrib import admin
from .models import Form

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user_type', 'created_at']
    list_filter = ['category', 'user_type']
    search_fields = ['title', 'description']