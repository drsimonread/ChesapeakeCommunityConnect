from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Member)

@admin.register(models.AccountCreation)
class AccountCreationAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'displayname', 'created')
    list_filter = ('created',)
    search_fields = ('email', 'username', 'displayname')
    ordering = ('created',)  # Oldest to newest
    readonly_fields = ('created',)

    fieldsets = (
        ('User Information', {
            'fields': ('email', 'username', 'displayname')
        }),
        ('Account Details', {
            'fields': ('password', 'confirmpassword')
        }),
        ('Request Information', {
            'fields': ('created',),
            'classes': ('collapse',)
        }),
    )