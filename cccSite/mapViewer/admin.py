from django.contrib import admin
from django.utils import timezone
from .models import *
# Register your models here.
admin.site.register(MapTag)

@admin.register(MapPost)
class MapPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visibility', 'get_created_date', 'get_tags')
    list_filter = ('visibility', 'tags', 'created')
    search_fields = ('title', 'content', 'description', 'author__username', 'author__displayname')
    ordering = ('created',)  # Oldest to newest
    readonly_fields = ('created',)
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'content', 'description', 'author')
        }),
        ('Location', {
            'fields': ('geoCode',)
        }),
        ('Post Settings', {
            'fields': ('tags', 'visibility', 'created')
        }),
    )
    
    def get_created_date(self, obj):
        """Format the created date in a human-readable format"""
        if obj.created:
            # Convert to local time and format in 12-hour format with AM/PM
            local_time = timezone.localtime(obj.created)
            return local_time.strftime('%Y-%m-%d %I:%M %p')
        return 'Not set'
    get_created_date.short_description = 'Created'
    get_created_date.admin_order_field = 'created'
    
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])
    get_tags.short_description = 'Tags'