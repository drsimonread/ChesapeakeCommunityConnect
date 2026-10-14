from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import MapTag

import googlemaps
import magic


def get_upload_attrs():
    """Return accepted MIME types for file upload widgets."""
    return ",".join(settings.VALID_UPLOAD_TYPES)


def validate_file(value):
    """Validate an uploaded file's MIME type."""
    if not value:
        return

    try:
        mime_type = magic.from_buffer(value.read(2048), mime=True)
    finally:
        value.seek(0)

    if mime_type not in settings.VALID_UPLOAD_TYPES:
        raise ValidationError(
            _("Unsupported file type."),
            code="filerr",
        )


def geocode_address(address):
    """Look up an address using Google Maps."""
    api_key = getattr(settings, "GOOGLE_MAPS_API_KEY", "")

    if not api_key:
        raise ValidationError(
            _("Address lookup is not configured."),
            code="geocode_config",
        )

    try:
        client = googlemaps.Client(key=api_key)
        results = client.geocode(address=address)
    except Exception as exc:
        raise ValidationError(
            _("Unable to look up this address. Please try again."),
            code="geocode_error",
        ) from exc

    if not results:
        raise ValidationError(
            _("Invalid address."),
            code="adderr",
        )

    return results


class SearchForumsForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        label=_("Search"),
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )

    t = forms.ModelMultipleChoiceField(
        queryset=MapTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_("Tags"),
    )


class MakeForumForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Title",
        widget=forms.TextInput(attrs={"placeholder": "Title"}),
    )

    firstName = forms.CharField(
        max_length=100,
        label="First",
        widget=forms.TextInput(attrs={"placeholder": "First"}),
    )

    lastName = forms.CharField(
        max_length=100,
        label="Last",
        widget=forms.TextInput(attrs={"placeholder": "Last"}),
    )

    location = forms.CharField(
        max_length=200,
        label="Address",
        widget=forms.TextInput(attrs={"placeholder": "Location"}),
    )

    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={"placeholder": "Content"}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=MapTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Tags",
        required=False,
    )

    geoResult = forms.JSONField(
        widget=forms.HiddenInput,
        required=False,
    )

    associated_choices = [
        ("associated", "I am associated with the group providing this solution"),
        ("not-associated", "I am not associated with the group providing this solution"),
    ]

    associated = forms.ChoiceField(
        choices=associated_choices,
        label="Association",
    )

    private_public_choices = [
        ("public", "Public (Anyone can view and add Posts)"),
        ("private", "Private (Only invited Contributors can view and add Posts)"),
    ]

    private_public = forms.ChoiceField(
        choices=private_public_choices,
        label="Visibility",
    )

    file1 = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"accept": get_upload_attrs()}
        ),
        required=False,
        validators=[validate_file],
    )

    file2 = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"accept": get_upload_attrs()}
        ),
        required=False,
        validators=[validate_file],
    )

    file3 = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"accept": get_upload_attrs()}
        ),
        required=False,
        validators=[validate_file],
    )

    file4 = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={"accept": get_upload_attrs()}
        ),
        required=False,
        validators=[validate_file],
    )

    def clean(self):
        cleaned_data = super().clean()

        location = cleaned_data.get("location")
        geo_result = cleaned_data.get("geoResult")

        if location and not geo_result:
            try:
                geo_result = geocode_address(location)
            except ValidationError as exc:
                self.add_error("location", exc)
                return cleaned_data

        cleaned_data["geoResult"] = geo_result

        cleaned_data["files"] = [
            cleaned_data.get("file1"),
            cleaned_data.get("file2"),
            cleaned_data.get("file3"),
            cleaned_data.get("file4"),
        ]

        return cleaned_data


class SearchPostsForm(forms.Form):
    q = forms.CharField(
        max_length=100,
        required=False,
        label=_("Search"),
        widget=forms.TextInput(attrs={"placeholder": "Search..."}),
    )

    t = forms.ModelMultipleChoiceField(
        queryset=MapTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_("Tags"),
    )


class MakePostForm(forms.Form):
    title = forms.CharField(
        max_length=100,
        label="Title",
        widget=forms.TextInput(attrs={"placeholder": "Title"}),
    )

    firstName = forms.CharField(
        max_length=100,
        label="First",
        widget=forms.TextInput(attrs={"placeholder": "First"}),
    )

    lastName = forms.CharField(
        max_length=100,
        label="Last",
        widget=forms.TextInput(attrs={"placeholder": "Last"}),
    )

    location = forms.CharField(
        max_length=200,
        label="Address",
        widget=forms.TextInput(attrs={"placeholder": "Location"}),
    )

    content = forms.CharField(
        label="Content",
        widget=forms.Textarea(attrs={"placeholder": "Content"}),
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=MapTag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Tags",
        required=False,
    )

    geoResult = forms.JSONField(
        widget=forms.HiddenInput,
        required=False,
    )

    media_file = forms.ImageField(
        required=False,
        label="Image",
    )

    def clean(self):
        cleaned_data = super().clean()

        location = cleaned_data.get("location")
        geo_result = cleaned_data.get("geoResult")

        if location and not geo_result:
            try:
                geo_result = geocode_address(location)
            except ValidationError as exc:
                self.add_error("location", exc)
                return cleaned_data

        cleaned_data["geoResult"] = geo_result

        return cleaned_data