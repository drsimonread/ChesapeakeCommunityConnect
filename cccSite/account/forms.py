from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError
from .models import Member  # make sure this import is here
from mapViewer.models import MapTag
import googlemaps



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

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("location"):
            return cleaned_data

        geo_result = cleaned_data.get("geoResult")
        if not geo_result:
            api_key = getattr(settings, "GOOGLE_API_KEY", "")
            if not api_key:
                raise ValidationError(
                    "The address could not be located. Please select an address suggestion."
                )
            results = googlemaps.Client(key=api_key).geocode(
                address=cleaned_data["location"]
            )
            if not results:
                raise ValidationError(
                    "The address could not be located. Please check the address and try again."
                )
            geo_result = results[0]

        cleaned_data["geoResult"] = geo_result
        return cleaned_data

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
        widget=forms.Select(attrs={
            "class": "contrib-search-select cc-field-input cc-field-input--select",
            "onchange": "this.form.submit()",
        }),
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
