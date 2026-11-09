from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member  # make sure this import is here
from mapViewer.models import MapTag


class CreateForumForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")
    firstName = forms.CharField(max_length=75, label="First name")
    lastName = forms.CharField(max_length=75, label="Last name")
    location = forms.CharField(max_length=200, label="Address")
    content = forms.CharField(label="Description", widget=forms.Textarea)
    tags = forms.ModelMultipleChoiceField(
        queryset=MapTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Topics",
    )
    associated = forms.ChoiceField(
        choices=(("yes", "Yes"), ("no", "No")),
        widget=forms.RadioSelect,
        label="Is this forum associated with an organization?",
    )
    private_public = forms.ChoiceField(
        choices=(("public", "Public"), ("private", "Private")),
        widget=forms.RadioSelect,
        label="Visibility",
    )
    file1 = forms.FileField(required=False, label="File 1")
    file2 = forms.FileField(required=False, label="File 2")
    file3 = forms.FileField(required=False, label="File 3")
    file4 = forms.FileField(required=False, label="File 4")
    geoResult = forms.JSONField(widget=forms.HiddenInput, required=False)

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
                "placeholder": "Type part of a username…",
                "autocomplete": "off",
                "inputmode": "search",
                "enterkeyhint": "search",
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
