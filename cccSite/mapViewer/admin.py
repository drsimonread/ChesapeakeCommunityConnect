from django.contrib import admin
from django.contrib import messages
from .models import *
# Register your models here.
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Media)


@admin.register(Forum)
class ForumAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'visibility_status', 'created_display', 'location_display')
    list_filter = ('visibility', 'private_public', 'associated')
    search_fields = ('title', 'content', 'author__user__username', 'author__user__email')
    readonly_fields = ('geoCode', 'description')
    filter_horizontal = ('tags', 'contributors')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'content', 'author', 'description')
        }),
        ('Location', {
            'fields': ('geoCode',)
        }),
        ('Settings', {
            'fields': ('visibility', 'private_public', 'associated', 'tags', 'contributors')
        }),
    )
    
    actions = ['approve_uploads', 'reject_uploads']
    
    def get_queryset(self, request):
        """Customize queryset - show all but make it easy to filter"""
        qs = super().get_queryset(request)
        return qs.select_related('author__user').prefetch_related('tags')
    
    def visibility_status(self, obj):
        """Display human-readable visibility status"""
        status_map = {
            -1: 'Denied',
            0: 'Pending',
            1: 'Visible'
        }
        return status_map.get(obj.visibility, 'Unknown')
    visibility_status.short_description = 'Status'
    
    def created_display(self, obj):
        """Display creation info if available"""
        # Forum model doesn't have created_at, but we can show author info
        if obj.author:
            return f"By {obj.author.user.username}"
        return "Unknown author"
    created_display.short_description = 'Author'
    
    def location_display(self, obj):
        """Display location from geoCode"""
        if obj.geoCode and isinstance(obj.geoCode, dict):
            # Try to get formatted address or location name
            return obj.geoCode.get('formatted_address', obj.geoCode.get('name', 'N/A'))
        return 'N/A'
    location_display.short_description = 'Location'
    
    def approve_uploads(self, request, queryset):
        """Approve selected upload requests (set visibility to visible)"""
        # Filter to only pending requests
        pending_forums = queryset.filter(visibility=0)
        approved_count = pending_forums.update(visibility=1)
        
        if approved_count > 0:
            self.message_user(
                request,
                f"Successfully approved {approved_count} upload request(s).",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "No pending uploads were selected. Please select pending uploads to approve.",
                messages.WARNING
            )
    
    approve_uploads.short_description = "Approve selected pending upload requests"
    
    def reject_uploads(self, request, queryset):
        """Reject selected upload requests (set visibility to denied)"""
        # Filter to only pending requests
        pending_forums = queryset.filter(visibility=0)
        rejected_count = pending_forums.update(visibility=-1)
        
        if rejected_count > 0:
            self.message_user(
                request,
                f"Successfully rejected {rejected_count} upload request(s).",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "No pending uploads were selected. Please select pending uploads to reject.",
                messages.WARNING
            )
    
    reject_uploads.short_description = "Reject selected pending upload requests"