#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
from django import forms
from .models import MapTag
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import googlemaps
from datetime import datetime


class SearchPostsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    t = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
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
    media_file = models.ImageField(upload_to='cccSite'/'media', required = False)  # Save files under media/uploads/

    #to minimize API calls, we don't want to geocode a provided address more than once. 
    #so if an address is correct, we want to use one geocode call to get the lat/long, but we can't just pass this to the model,
    #because if the provided address doesn't result in a valid geocode, we can't try to access said geocode. this stores a valid geocode
    #in the geoResult field of the form, and  also builds in an error message to the address code if there is no geocode
    def clean(self): 
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc') #initialize maps
        cleaned_data = super().clean() #verify that all the other forms are ok
        if not self.cleaned_data['geoResult']: #if we don't have a geocode (first try or last try was invalid)
            geoResult=gmaps.geocode(address=self.cleaned_data['location']) #fetch geocode for provided address (API call)
            if not geoResult: #if still none, then the address is invalid
                raise ValidationError(_("Invalid Address"), code="adderr")
        print(geoResult)
        return {'title': self.cleaned_data['title'],
                'location': self.cleaned_data['location'],
                'content': self.cleaned_data['content'],
                'tags': self.cleaned_data['tags'],
                'geoResult': geoResult,
                'media_file': self.cleaned_data['media_file']}  # Include media file in cleaned data#return a dictionary of cleaned_data
        
    def _clean_form(self): #when we check is_valid, this occurs
        try:
            cleaned_data = self.clean() #try to clean the data
        except ValidationError as e:
            self.add_error('location', e) #if we get the error of invalid address, attach it to the location field
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data #if successful, store in cleaned_data


