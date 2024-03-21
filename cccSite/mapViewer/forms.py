#https://medium.com/swlh/django-forms-for-many-to-many-fields-d977dec4b024
from django import forms
from django.conf import settings
from .models import MapTag
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import googlemaps
from django.db import models
from datetime import datetime
import magic


class SearchPostsForm(forms.Form):
    q = forms.CharField(max_length=100, required=False, widget=forms.TextInput({"Placeholder": "Search..."}))
    t = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        labels = {
                'q': _('Search'),
                't': _('Tags')
            }



#post creation form
class MakePostForm(forms.Form):
    def get_upload_attrs():#function that converts the list of accepted file types to a string for use in restricting what is selectable in the upload interface
        val = '' #start blank
        for item in settings.VALID_UPLOAD_TYPES: #for valid file type
            val = '{0},{1}'.format(val, item) #add to string
        return val
    def validate_file(value): #validator that verifies that uploaded file is of an accepted type. if not, raise validation error
        if magic.from_buffer(value.read(), mime=True) not in settings.VALID_UPLOAD_TYPES:
                raise ValidationError(_("Bad file"), code="filerr")


    title = forms.CharField(max_length=100, label="Title") #title of post
    location = forms.CharField(max_length=200, label="Address", widget=forms.TextInput) #location of post as an address
    content = forms.CharField(label="Content", widget=forms.Textarea) #content of the post
    tags = forms.ModelMultipleChoiceField(queryset=MapTag.objects.all(), widget=forms.CheckboxSelectMultiple, label="Tags", required = False)#tags of post
    geoResult = forms.JSONField(widget=forms.HiddenInput, required=False)#hidden field for converting from user provided address to google's geocode
    #the file upload fields. validated using the custom validator above, if left empty or if a bad file is submitted, these fields have nothing in them
    file1 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    file2 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    file3 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    file4 = forms.FileField(widget=forms.ClearableFileInput(attrs={'accept':get_upload_attrs()}), required=False, validators=[validate_file])
    

    

    
    #to minimize API calls, we don't want to geocode a provided address more than once. 
    #so if an address is correct, we want to use one geocode call to get the lat/long, but we can't just pass this to the model,
    #because if the provided address doesn't result in a valid geocode, we can't try to access said geocode. this stores a valid geocode
    #in the geoResult field of the form, and  also builds in an error message to the address code if there is no geocode
    def clean(self): 
        gmaps = googlemaps.Client(key='AIzaSyAH_5F4XRcZh8_OZib8cUD-DoE7ust60lc') #initialize maps
        cleaned_data = super().clean() #verify that all the other fields are ok
        if not cleaned_data['geoResult']: #if we don't have a geocode (first try or last try was invalid)
            geoResult=gmaps.geocode(address=self.cleaned_data['location']) #fetch geocode for provided address (API call)
            if not geoResult: #if still none, then the address is invalid
                raise ValidationError(_("Invalid Address"), code="adderr")
        print(geoResult)
        return {'title': cleaned_data['title'],
                'location': cleaned_data['location'],
                'content': cleaned_data['content'],
                'tags': cleaned_data['tags'],
                'geoResult': geoResult,
                'files': [cleaned_data.get('file1'),cleaned_data.get('file2'),cleaned_data.get('file3'),cleaned_data.get('file4')],
                }  # if a file is legit, the .get returns the file. if not (or if it doesn't exist), 
                # the .get returns None, and so we can iterate through cleaned_data['files'] in a view, and check if an entry isn't None to 
                # see if we have a file to save or not
        
    def _clean_form(self): #when we check is_valid, this occurs
        try:
            cleaned_data = self.clean() #try to clean the data
        except ValidationError as e:
            match e.code:
                case "adderr":
                    self.add_error('location', e) #if we get the error of invalid address, attach it to the location field
                case "filerr":
                    self.add_error('file1', e) #if we get a file error, attach it to the first file field.
            
        else:
            if cleaned_data is not None:
                self.cleaned_data = cleaned_data #if successful, store in cleaned_data


