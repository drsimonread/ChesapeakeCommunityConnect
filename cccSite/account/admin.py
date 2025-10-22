from django.contrib import admin
from django.contrib import messages
from . import models

# Register your models here.
admin.site.register(models.Member)

@admin.register(models.AccountCreation)
class AccountCreationAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'displayname', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('email', 'username', 'displayname')
    ordering = ('created',)  # Oldest to newest
    readonly_fields = ('created',)
    actions = ['accept_requests', 'reject_requests']

    fieldsets = (
        ('User Information', {
            'fields': ('email', 'username', 'displayname')
        }),
        ('Account Details', {
            'fields': ('password', 'confirmpassword')
        }),
        ('Request Status', {
            'fields': ('status',)
        }),
        ('Request Information', {
            'fields': ('created',),
            'classes': ('collapse',)
        }),
    )

    def accept_requests(self, request, queryset):
        """Accept selected account requests"""
        updated = queryset.filter(status='pending').update(status='accepted')
        if updated:
            self.message_user(request, f'{updated} account request(s) were accepted.', messages.SUCCESS)
        else:
            self.message_user(request, 'No pending requests were selected.', messages.WARNING)
    accept_requests.short_description = "Accept selected account requests"

    def reject_requests(self, request, queryset):
        """Reject selected account requests"""
        updated = queryset.filter(status='pending').update(status='rejected')
        if updated:
            self.message_user(request, f'{updated} account request(s) were rejected.', messages.SUCCESS)
        else:
            self.message_user(request, 'No pending requests were selected.', messages.WARNING)
    reject_requests.short_description = "Reject selected account requests"