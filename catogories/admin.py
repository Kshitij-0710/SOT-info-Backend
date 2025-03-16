from django.contrib import admin
from .models import Form

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user_type', 'created_at', 'is_top_6']
    list_filter = ['category', 'user_type', 'is_top_6']
    search_fields = ['title', 'description', 'category', 'achivements']