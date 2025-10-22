from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Member)

@admin.register(models.AccountCreation)
class AccountCreationAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'displayname')
    search_fields = ('email', 'username', 'displayname')
    
    fieldsets = (
        ('User Information', {
            'fields': ('email', 'username', 'displayname')
        }),
        ('Account Details', {
            'fields': ('password', 'confirmpassword')
        }),
    )