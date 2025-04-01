from django.contrib import admin
from .models import LinkedInEmbeds

@admin.register(LinkedInEmbeds)
class LinkedInEmbedsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'updated_at')
    readonly_fields = ('preview',)
    fieldsets = (
        (None, {
            'fields': ('embed_code',),
            'description': 'Enter LinkedIn embed URLs separated by commas'
        }),
        ('Preview', {
            'fields': ('preview',),
            'classes': ('collapse',),
        }),
    )
    
    def has_add_permission(self, request):
        # Check if any embed instances exist
        count = LinkedInEmbeds.objects.count()
        if count == 0:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        return False