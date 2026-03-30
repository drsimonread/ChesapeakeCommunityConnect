from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member  # make sure this import is here

class SearchAccountForm(forms.Form):
    CHOICES = (
        ('0','A-Z'),
        ('1','Z-A'),
        ('2','# of forums, high-low'),
        ('3','# of forums, low-high'),
    )
    q = forms.CharField(
        label='Search by name',
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "contrib-search-input cc-field-input",
                "placeholder": "Search by username…",
                "autocomplete": "off",
            }
        ),
    )
    s = forms.ChoiceField(
        label='Sort by',
        choices=CHOICES,
        required=False,
        widget=forms.Select(attrs={"class": "contrib-search-select cc-field-input cc-field-input--select"}),
    )

class CreateAccountForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()

        member = Member.objects.create(user=user)

        return user, member
