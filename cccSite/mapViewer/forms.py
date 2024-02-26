#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
from django import forms
from .models import MapTag
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import googlemaps
from datetime import datetime


class SearchPostsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, label="Search")
    t = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False, label="Tags")
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }





class MakePostForm(forms.Form):
    title = forms.CharField(max_length=100, label="Title")
    location = forms.CharField(max_length=200, label="Address", widget=forms.TextInput)
    content = forms.CharField(label="Content", widget=forms.Textarea)
    tags = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tags", required = False)
    geoResult = forms.JSONField(widget=forms.HiddenInput, required=False)
    def clean(self):
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc')
        cleaned_data = super().clean()
        if not geoResult:
            geoResult=gmaps.geocode(address=self.cleaned_data['location'])
            if not geoResult:
                raise ValidationError(_("Invalid Address"), code="adderr")
        return {'title': self.cleaned_data['title'],
                'location': self.cleaned_data['location'],
                'content': self.cleaned_data['content'],
                'tags': self.cleaned_data['tags'],
                'geoResult': geoResult}
    def _clean_form(self):
        try:
            cleaned_data = self.clean()
        except ValidationError as e:
            self.add_error('location', e)
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data


