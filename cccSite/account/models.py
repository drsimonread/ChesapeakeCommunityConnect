from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, EmailInput, PasswordInput, Textarea
from django.urls import reverse
from .storage import OverwriteStorage
from django.utils.translation import gettext_lazy as _


#function used for saving images
def user_directory_profile(instance, filename): 
    # file will be uploaded to MEDIA_ROOT / users / <pk> / profile.<ext>
    ext = filename.split('.')[-1]
    filename="profile."+ext
    return 'users/{0}/{1}'.format(instance.pk, filename) 

# user model. self explanitory

# MEMBER_DELETE
class Member(models.Model):
    # name = models.CharField(max_length=35)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ranking_options = { 
        (-1,"banned"),
        (1 , "member"),
        (2 , "trusted member"),
        (98 , "moderator"),
        (99 , "admin"),
    }
    ranking = models.SmallIntegerField(default=1, choices=ranking_options)
    # created = models.DateTimeField(auto_now=False, auto_now_add=True)
    # email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, default="")
    pic = models.ImageField(upload_to=user_directory_profile, storage = OverwriteStorage(), default='default/blankprof.png')
    about = models.TextField(blank=True, default="")
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

   #location
    def __str__(self):
        return self.user.username
    @property
    def get_absolute_url(self):
        return reverse("account:account_view", args=[str(self.pk)])
    @property
    def get_admin_url(self):
        return reverse("Janitor:manage_user", args=[str(self.pk)])
    #https://stackoverflow.com/questions/3715103/password-field-in-django-model/3715382#3715382 for making own password


# when user logs in with google, check the given google ID against this and then authenticate as user that is pointed to
# same pattern can be used to implement other log in methods
class GLogIn(models.Model):
    googleID = models.CharField(max_length=255, unique=True)
    # MEMBER_DELETE
    referTo = models.ForeignKey(Member, on_delete = models.CASCADE)
    def __str__(self):
        return self.googleID + "|" + str(self.referTo)

class ManageForm(ModelForm):
    class Meta:
        # MEMBER_DELETE
        model = Member
        fields = ["pic", "phone_number", "about"]

        widgets = {
            "phone_number": forms.TextInput(
                attrs={
                    "class": "account-form-input cc-field-input",
                    "placeholder": "Optional",
                    "autocomplete": "tel",
                    "maxlength": "20",
                }
            ),
            "about": forms.Textarea(
                attrs={
                    "class": "account-form-textarea cc-field-input",
                    "rows": 5,
                    "placeholder": "Tell others a bit about yourself or your organization…",
                }
            ),
        }
        labels = {
            "pic": "Profile photo",
            "phone_number": "Phone number",
            "about": "About you",
        }
        help_texts = {
            "pic": "JPEG or PNG recommended. Square images work best.",
            "phone_number": "Optional. Shown only where you choose to share it.",
            "about": "A short bio or description for your contributor page.",
        }
        


class UPLogIn(models.Model):
    # MEMBER_DELETE
    referTo = models.ForeignKey(Member, on_delete = models.CASCADE)
    username = models.CharField(max_length=35, unique=True)
    salt = models.CharField(max_length=22)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username + " | " + self.referTo.name


class AccountCreation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    email = models.EmailField()
    username = models.CharField(max_length=75)
    displayname = models.CharField(max_length=75)
    password = models.CharField(max_length=50)
    confirmpassword = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'User Request'
        verbose_name_plural = 'User Requests'
    
    def __str__(self):
        return self.email + " | " + self.username + " | " + self.displayname
    
class MessageForm(ModelForm):
    class Meta:
        model = AccountCreation
        fields = ['email', 'username', 'displayname', 'password', 'confirmpassword']
        labels = {
            "email": _("Email"),
            "username": _("Username"),
            "displayname": _("Displayname"),
            
        }
        widgets = {
            'email': EmailInput(attrs={'placeholder': 'Email address', 'class': 'input-text'}),
            'username': TextInput(attrs={'placeholder': 'Username', 'class': 'input-text'}),
            'displayname': TextInput(attrs={'placeholder': 'Displayname', 'class': 'input-text'}),
            'password': PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-text'}),
            'confirmpassword': PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-text'}),
        }
