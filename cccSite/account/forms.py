from django import forms
from django.utils.translation import gettext_lazy as _

class SearchAccountForm(forms.Form):
    CHOICES = (
        ('0','A-Z'),
        ('1','Z-A'),
        ('2','# of forums, high-low'),
        ('3','# of forums, low-high'),
    )
    q = forms.CharField(label='Search', max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    s = forms.CharField(label='Sort By', widget=forms.Select(choices=CHOICES), required=False)

class CreateAccountForm(forms.Form):
    username = forms.CharField(max_length=25, widget=forms.TextInput({'Placeholder' : "User Name"}))
    email = forms.EmailField(widget=forms.TextInput({'Placeholder' : "Email"}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput({'Placeholder' : "Password"}))
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput({'Placeholder' : "Confirm Password"}))
    