from django.contrib import admin
<<<<<<< HEAD
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
=======
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.html import format_html
from django.urls import reverse
from django import forms
from . import models

# Register your models here.


class MemberAdminForm(forms.ModelForm):
    """Custom form to include User model fields"""
    first_name = forms.CharField(max_length=150, required=False, label='First Name')
    last_name = forms.CharField(max_length=150, required=False, label='Last Name')
    email = forms.EmailField(required=False, label='Email')
    is_active = forms.BooleanField(required=False, label='Active')
    
    class Meta:
        model = models.Member
        fields = ['phone_number', 'about', 'pic', 'ranking']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['is_active'].initial = self.instance.user.is_active
    
    def save(self, commit=True):
        member = super().save(commit=commit)
        if commit and member.user:
            member.user.first_name = self.cleaned_data.get('first_name', '')
            member.user.last_name = self.cleaned_data.get('last_name', '')
            member.user.email = self.cleaned_data.get('email', '')
            member.user.is_active = self.cleaned_data.get('is_active', True)
            member.user.save()
        return member


@admin.register(models.Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin interface for Current Users - shows active users"""
    form = MemberAdminForm
    list_display = ('username', 'full_name', 'email', 'phone_number', 'ranking_display', 'is_active_status', 'date_joined', 'edit_button')
    list_filter = ('ranking', 'user__is_active', 'user__date_joined')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone_number')
    readonly_fields = ('username_display', 'get_date_joined')
    ordering = ('-user__date_joined',)
    
    fieldsets = (
        ('User Account Information', {
            'fields': ('username_display', 'first_name', 'last_name', 'email', 'is_active', 'get_date_joined')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'about')
        }),
        ('Profile', {
            'fields': ('pic',)
        }),
        ('Account Settings', {
            'fields': ('ranking',)
        }),
    )
    
    def username(self, obj):
        """Display username"""
        return obj.user.username
    username.short_description = 'Username'
    username.admin_order_field = 'user__username'
    
    def full_name(self, obj):
        """Display full name"""
        first = obj.user.first_name or ''
        last = obj.user.last_name or ''
        if first or last:
            return f"{first} {last}".strip()
        return '-'
    full_name.short_description = 'Name'
    full_name.admin_order_field = 'user__first_name'
    
    def email(self, obj):
        """Display email"""
        return obj.user.email
    email.short_description = 'Email'
    email.admin_order_field = 'user__email'
    
    def phone_number(self, obj):
        """Display phone number"""
        return obj.phone_number if obj.phone_number else '-'
    phone_number.short_description = 'Phone Number'
    
    def ranking_display(self, obj):
        """Display human-readable ranking"""
        ranking_map = {
            -1: 'Banned',
            1: 'Member',
            2: 'Trusted Member',
            98: 'Moderator',
            99: 'Admin'
        }
        return ranking_map.get(obj.ranking, 'Unknown')
    ranking_display.short_description = 'Ranking'
    ranking_display.admin_order_field = 'ranking'
    
    def is_active_status(self, obj):
        """Display active status"""
        return 'Active' if obj.user.is_active else 'Inactive'
    is_active_status.short_description = 'Status'
    is_active_status.admin_order_field = 'user__is_active'
    
    def date_joined(self, obj):
        """Display date joined"""
        return obj.user.date_joined
    date_joined.short_description = 'Date Joined'
    date_joined.admin_order_field = 'user__date_joined'
    
    def edit_button(self, obj):
        """Display Edit button"""
        url = reverse('admin:account_member_change', args=[obj.pk])
        return format_html('<a class="button" href="{}">Edit</a>', url)
    edit_button.short_description = 'Actions'
    edit_button.allow_tags = True
    
    def username_display(self, obj):
        """Read-only username field"""
        return obj.user.username if obj.user else '-'
    username_display.short_description = 'Username'
    
    def get_date_joined(self, obj):
        """Read-only date joined field"""
        return obj.user.date_joined if obj.user else '-'
    get_date_joined.short_description = 'Date Joined'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')


@admin.register(models.AccountCreation)
class AccountCreationAdmin(admin.ModelAdmin):
    """Admin interface for User Requests - shows pending account requests"""
    list_display = ('username', 'email', 'displayname', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('username', 'email', 'displayname')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    fieldsets = (
        ('User Information', {
            'fields': ('username', 'email', 'displayname')
        }),
        ('Password Information', {
            'fields': ('password', 'confirmpassword')
        }),
        ('Status', {
            'fields': ('status', 'created_at')
        }),
    )
    
    actions = ['accept_requests', 'reject_requests']
    
    def accept_requests(self, request, queryset):
        """Accept selected account requests and create user accounts"""
        accepted_count = 0
        errors = []
        
        for account_request in queryset.filter(status='pending'):
            try:
                # Check if username or email already exists
                if User.objects.filter(username=account_request.username).exists():
                    errors.append(f"Username '{account_request.username}' already exists")
                    continue
                if User.objects.filter(email=account_request.email).exists():
                    errors.append(f"Email '{account_request.email}' already exists")
                    continue
                
                # Create the User
                user = User.objects.create_user(
                    username=account_request.username,
                    email=account_request.email,
                    password=account_request.password
                )
                
                # Create the Member
                member = models.Member.objects.create(user=user)
                
                # Mark request as approved
                account_request.status = 'approved'
                account_request.save()
                
                accepted_count += 1
            except Exception as e:
                errors.append(f"Error processing {account_request.username}: {str(e)}")
        
        if accepted_count > 0:
            self.message_user(
                request,
                f"Successfully accepted {accepted_count} account request(s).",
                messages.SUCCESS
            )
        
        if errors:
            for error in errors:
                self.message_user(request, error, messages.ERROR)
    
    accept_requests.short_description = "Accept selected account requests"
    
    def reject_requests(self, request, queryset):
        """Reject selected account requests"""
        rejected_count = queryset.filter(status='pending').update(status='rejected')
        self.message_user(
            request,
            f"Successfully rejected {rejected_count} account request(s).",
            messages.SUCCESS
        )
    
    reject_requests.short_description = "Reject selected account requests"
    
    def get_queryset(self, request):
        """Customize the queryset to show all requests"""
        qs = super().get_queryset(request)
        return qs
>>>>>>> 9217a0dea934062225358f845c7b8cc6a98cc31e
