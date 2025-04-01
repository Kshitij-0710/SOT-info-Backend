from django.contrib import admin
from .models import Form,Placement,Event

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'user_type', 'created_at', 'is_top_6','is_ongoing']
    list_filter = ['category', 'user_type', 'is_top_6','is_ongoing']
    search_fields = ['title', 'description', 'category', 'achivements']


@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ['title', 'student', 'company', 'package', 'date','top_2']
    list_filter = ['company', 'date','top_2']
    search_fields = ['title', 'description', 'company', 'student','top_2']
@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    list_display = ['title','date','location']