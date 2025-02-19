from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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

class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        
    # def __init__(self, *args, **kwargs):
    #     super(CreateAccountForm, self).__init__(*args, **kwargs)
    #     print("test5")
    #     if self.data:
    #         print("test6")
    #         # Optionally, set initial values here if needed
    #         self.fields["username"].initial = self.data.get("username")
    #         self.fields["email"].initial = self.data.get("email")
    #         self.fields["password"].initial = self.data.get("password")
    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(UserCreationForm, self).save(commit=True)
        user.email = self.cleaned_data["email"]
        member = Member.objects.create(user=user)
        
        return user, member
    
            

    