from django import forms
from django.contrib import admin
from django.contrib import messages
from . import models
from .services import approve_signup


# Register your models here.
admin.site.register(models.Member)


class AccountCreationAdminForm(forms.ModelForm):
    new_password = forms.CharField(
        max_length=models.AccountCreation.MAX_PASSWORD_LENGTH,
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    confirm_password = forms.CharField(
        max_length=models.AccountCreation.MAX_PASSWORD_LENGTH,
        required=False,
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("new_password")
        if not password and self.instance._state.adding:
            self.add_error("new_password", "Enter a password.")
        elif password != cleaned_data.get("confirm_password"):
            self.add_error("confirm_password", "The passwords do not match.")
        return cleaned_data


@admin.register(models.AccountCreation)
class AccountCreationAdmin(admin.ModelAdmin):
    form = AccountCreationAdminForm
    list_display = ('email', 'username', 'displayname', 'email_verified', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('email', 'username', 'displayname')
    ordering = ('created',)  # Oldest to newest
    readonly_fields = ('created', 'email_verified', 'member', 'status')
    actions = ['accept_requests', 'reject_requests']

    fieldsets = (
        ('User Information', {
            'fields': ('email', 'username', 'displayname')
        }),
        ('Account Details', {
            'fields': ('new_password', 'confirm_password')
        }),
        ('Request Status', {
            'fields': ('email_verified', 'status', 'member')
        }),
        ('Request Information', {
            'fields': ('created',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data["new_password"]
        if password:
            obj.set_password(password)
        if change:
            update_fields = [
                field for field in form.changed_data
                if field not in ("new_password", "confirm_password")
            ]
            if password:
                update_fields.append("password")
            obj.save(update_fields=update_fields)
        else:
            super().save_model(request, obj, form, change)

    def accept_requests(self, request, queryset):
        pending = list(queryset.filter(status="pending"))
        accepted = sum(approve_signup(account) for account in pending)
        skipped = len(pending) - accepted
        if accepted:
            self.message_user(request, f'{accepted} verified account request(s) were approved.', messages.SUCCESS)
        if skipped:
            self.message_user(
                request,
                f'{skipped} request(s) were not approved because the email is unverified or already belongs to a member.',
                messages.WARNING,
            )
        if not accepted and not skipped:
            self.message_user(request, 'No pending account requests were selected.', messages.WARNING)
    accept_requests.short_description = "Accept selected account requests"

    def reject_requests(self, request, queryset):
        """Reject selected account requests"""
        updated = queryset.filter(status='pending').update(status='rejected')
        if updated:
            self.message_user(request, f'{updated} account request(s) were rejected.', messages.SUCCESS)
        else:
            self.message_user(request, 'No pending requests were selected.', messages.WARNING)
    reject_requests.short_description = "Reject selected account requests"
