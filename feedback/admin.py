from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'thoughts_preview', 'user', 'order', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['name', 'thoughts', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def thoughts_preview(self, obj):
        return obj.thoughts[:50] + '...' if len(obj.thoughts) > 50 else obj.thoughts
    thoughts_preview.short_description = 'Thoughts Preview'